#!/usr/bin/env python3
"""
BMAD Skill: macOS Notes Integration

Integrates with native macOS Notes app via AppleScript.
Target folder: openhands-bmad-agents
"""

import subprocess
import json
import argparse
from typing import Optional, List


def run_applescript(script: str) -> str:
    """Execute AppleScript and return output."""
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
        f.write(script)
        script_path = f.name
    
    try:
        result = subprocess.run(
            ['osascript', script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(f"AppleScript error: {result.stderr}")
        return result.stdout.strip()
    finally:
        os.unlink(script_path)


def list_notes(folder: str = "openhands-bmad-agents", 
               filter_tags: Optional[List[str]] = None,
               limit: int = 50) -> List[dict]:
    """List all notes in the folder."""
    # Use JSON-like format for easier parsing
    script = f'''tell application "Notes"
    tell folder "{folder}"
        set resultList to ""
        repeat with n from 1 to count of notes
            set noteRef to item n of notes
            set noteName to name of noteRef
            set noteBody to body of noteRef
            set noteId to id of noteRef
            set noteMod to modification date of noteRef as string
            
            if resultList is not "" then
                set resultList to resultList & "<<<NOTE>>>"
            end if
            set resultList to resultList & noteName & "<<<SEP>>>" & noteBody & "<<<SEP>>>" & noteId & "<<<SEP>>>" & noteMod
            
            if n >= {limit} then exit repeat
        end repeat
        return resultList
    end tell
end tell'''
    
    result = run_applescript(script)
    if not result or result == "missing value":
        return []
    
    notes = []
    for note_str in result.split('<<<NOTE>>>'):
        parts = note_str.split('<<<SEP>>>')
        if len(parts) >= 3:
            note = {
                'name': parts[0].strip(),
                'body': parts[1].strip() if len(parts) > 1 else '',
                'id': parts[2].strip() if len(parts) > 2 else '',
                'modified': parts[3].strip() if len(parts) > 3 else ''
            }
            
            # Filter by tags if specified
            if filter_tags:
                body_lower = note['body'].lower()
                if not any(f'#{tag.lower()}' in body_lower for tag in filter_tags):
                    continue
            
            notes.append(note)
    
    return notes


def get_note(note_id: str, folder: str = "openhands-bmad-agents") -> Optional[dict]:
    """Get a specific note by ID."""
    script = f'''tell application "Notes"
    tell folder "{folder}"
        set noteList to notes where id = "{note_id}"
        if (count of noteList) = 0 then
            return "NOT_FOUND"
        else
            set noteRef to item 1 of noteList
            return name of noteRef & "|||BODY|||" & body of noteRef & "|||ID|||" & id of noteRef & "|||MOD|||" & (modification date of noteRef as string)
        end if
    end tell
end tell'''
    
    result = run_applescript(script)
    if result == "NOT_FOUND":
        return None
    
    parts = result.split('|||BODY|||')
    if len(parts) >= 2:
        return {
            'name': parts[0],
            'body': parts[1].split('|||ID|||')[0],
            'id': parts[1].split('|||ID|||')[1].split('|||MOD|||')[0],
            'modified': parts[1].split('|||MOD|||')[1]
        }
    return None


def add_note(name: str, body: str = "", tags: Optional[List[str]] = None,
             folder: str = "openhands-bmad-agents") -> dict:
    """Create a new note."""
    # Add tags to body
    full_body = body
    if tags:
        tag_str = ' '.join(f'#{tag}' for tag in tags)
        if full_body:
            full_body += f'\n\n{tag_str}'
        else:
            full_body = tag_str
    
    # Escape quotes
    full_body = full_body.replace('"', '\\"')
    name = name.replace('"', '\\"')
    
    script = f'''tell application "Notes"
    tell folder "{folder}"
        make new note at end with properties {{name:"{name}", body:"{full_body}"}}
        return id of result
    end tell
end tell'''
    
    note_id = run_applescript(script)
    return {
        'status': 'created',
        'id': note_id,
        'name': name
    }


def update_note(note_id: str, name: Optional[str] = None, body: Optional[str] = None,
                add_tags: Optional[List[str]] = None, folder: str = "openhands-bmad-agents") -> dict:
    """Update an existing note."""
    script = f'''tell application "Notes"
    tell folder "{folder}"
        set noteList to notes where id = "{note_id}"
        if (count of noteList) = 0 then
            return "NOT_FOUND"
        end if
        set noteRef to item 1 of noteList'''
    
    if name:
        escaped_name = name.replace('"', '\\"')
        script += f'\n        set name of noteRef to "{escaped_name}"'
    
    if body is not None:
        escaped_body = body.replace('"', '\\"')
        script += f'\n        set body of noteRef to "{escaped_body}"'
    
    if add_tags:
        for tag in add_tags:
            script += f'\n        set body of noteRef to (body of noteRef & " #{tag}")'
    
    script += '''
    end tell
end tell'''
    
    result = run_applescript(script)
    return {
        'status': 'updated' if result != 'NOT_FOUND' else 'not_found',
        'id': note_id
    }


def delete_note(note_id: str, folder: str = "openhands-bmad-agents") -> dict:
    """Delete a note."""
    script = f'''tell application "Notes"
    tell folder "{folder}"
        set noteList to notes where id = "{note_id}"
        if (count of noteList) = 0 then
            return "NOT_FOUND"
        end if
        delete item 1 of noteList
        return "DELETED"
    end tell
end tell'''
    
    result = run_applescript(script)
    return {
        'status': 'deleted' if result == 'DELETED' else 'not_found',
        'id': note_id
    }


def search_notes(query: str, folder: str = "openhands-bmad-agents", 
                 limit: int = 50) -> List[dict]:
    """Search notes by name or body content."""
    script = f'''tell application "Notes"
    tell folder "{folder}"
        set resultList to ""
        repeat with n from 1 to count of notes
            set noteRef to item n of notes
            set noteName to name of noteRef
            set noteBody to body of noteRef
            set noteMod to modification date of noteRef as string
            
            if (noteName contains "{query}") or (noteBody contains "{query}") then
                if resultList is not "" then
                    set resultList to resultList & "<<<NOTE>>>"
                end if
                set resultList to resultList & noteName & "<<<SEP>>>" & noteBody & "<<<SEP>>>" & id of noteRef & "<<<SEP>>>" & noteMod
            end if
            
            if n >= {limit} then exit repeat
        end repeat
        return resultList
    end tell
end tell'''
    
    result = run_applescript(script)
    if not result or result == "missing value":
        return []
    
    notes = []
    for note_str in result.split('<<<NOTE>>>'):
        parts = note_str.split('<<<SEP>>>')
        if len(parts) >= 3:
            notes.append({
                'name': parts[0].strip(),
                'body': parts[1].strip() if len(parts) > 1 else '',
                'id': parts[2].strip() if len(parts) > 2 else '',
                'modified': parts[3].strip() if len(parts) > 3 else ''
            })
    
    return notes


# CLI Interface
def main():
    parser = argparse.ArgumentParser(description='macOS Notes CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List
    list_parser = subparsers.add_parser('list', help='List notes')
    list_parser.add_argument('--folder', default='openhands-bmad-agents')
    list_parser.add_argument('--filter-tags', nargs='+', help='Filter by tags')
    list_parser.add_argument('--limit', type=int, default=50)
    
    # Get
    get_parser = subparsers.add_parser('get', help='Get note details')
    get_parser.add_argument('note_id', help='Note ID')
    get_parser.add_argument('--folder', default='openhands-bmad-agents')
    
    # Add
    add_parser = subparsers.add_parser('add', help='Create note')
    add_parser.add_argument('--name', required=True, help='Note name')
    add_parser.add_argument('--body', default='', help='Note body')
    add_parser.add_argument('--tags', nargs='+', help='Tags (without #)')
    add_parser.add_argument('--folder', default='openhands-bmad-agents')
    
    # Update
    update_parser = subparsers.add_parser('update', help='Update note')
    update_parser.add_argument('note_id', help='Note ID')
    update_parser.add_argument('--name', help='New name')
    update_parser.add_argument('--body', help='New body')
    update_parser.add_argument('--add-tags', nargs='+', help='Tags to add')
    update_parser.add_argument('--folder', default='openhands-bmad-agents')
    
    # Delete
    delete_parser = subparsers.add_parser('delete', help='Delete note')
    delete_parser.add_argument('note_id', help='Note ID')
    delete_parser.add_argument('--folder', default='openhands-bmad-agents')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Search notes')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--folder', default='openhands-bmad-agents')
    search_parser.add_argument('--limit', type=int, default=50)
    
    args = parser.parse_args()
    
    try:
        if args.command == 'list':
            notes = list_notes(args.folder, args.filter_tags, args.limit)
            print(json.dumps(notes, ensure_ascii=False, indent=2))
        
        elif args.command == 'get':
            note = get_note(args.note_id, args.folder)
            if note:
                print(json.dumps(note, ensure_ascii=False, indent=2))
            else:
                print(json.dumps({'error': 'Note not found'}, ensure_ascii=False))
        
        elif args.command == 'add':
            result = add_note(args.name, args.body, args.tags, args.folder)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif args.command == 'update':
            result = update_note(args.note_id, args.name, args.body, args.add_tags, args.folder)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif args.command == 'delete':
            result = delete_note(args.note_id, args.folder)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
        elif args.command == 'search':
            notes = search_notes(args.query, args.folder, args.limit)
            print(json.dumps(notes, ensure_ascii=False, indent=2))
        
        else:
            parser.print_help()
    except Exception as e:
        print(json.dumps({'error': str(e)}, ensure_ascii=False))


if __name__ == '__main__':
    main()