#!/usr/bin/env python3
"""macOS Reminders CLI Tool for OpenHands BMAD Agents

Provides full CRUD operations for Reminders app via AppleScript.
List: openhands-bmad-agents
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from typing import Optional


def run_applescript(script: str) -> str:
    """Execute AppleScript and return output."""
    import tempfile
    import os
    
    # Write script to temp file for complex scripts
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


def add_reminder(
    name: str,
    body: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    priority: int = 0,
    flagged: bool = False,
    tags: Optional[list] = None
) -> dict:
    """Create a new reminder."""
    
    # Escape double quotes in name
    safe_name = name.replace('"', '\\"')
    
    # Build body with tags
    body_parts = []
    if body:
        body_parts.append(body)
    if tags:
        # Avoid duplicating tags that might already be in body
        existing_tags = set()
        if body:
            import re
            existing_tags = set(re.findall(r'#\w+', body.lower()))
        
        for tag in tags:
            tag_formatted = '#' + tag if not tag.startswith('#') else tag
            if tag_formatted.lower() not in existing_tags:
                body_parts.append(tag_formatted)
    
    full_body = ' '.join(body_parts) if body_parts else ''
    safe_body = full_body.replace('"', '\\"') if full_body else ''
    
    # Build AppleScript
    script = 'tell application "Reminders"\n'
    script += '    tell list "openhands-bmad-agents"\n'
    script += '        set newReminder to make new reminder with properties {name:"' + safe_name + '"'
    
    if safe_body:
        script += ', body:"' + safe_body + '"'
    
    script += '}\n'
    
    if due_date and due_time:
        script += '        set due date of newReminder to date "' + due_date + ' ' + due_time + ':00"\n'
    elif due_date:
        script += '        set allday due date of newReminder to date "' + due_date + '"\n'
    
    if priority > 0:
        script += '        set priority of newReminder to ' + str(priority) + '\n'
    
    script += '        set flagged of newReminder to ' + ('true' if flagged else 'false') + '\n'
    script += '    end tell\n'
    script += 'end tell'
    
    run_applescript(script)
    
    return {"status": "created", "name": name}


def list_reminders(
    filter_tags: Optional[list] = None,
    filter_flagged: Optional[bool] = None,
    filter_completed: str = "all",
    limit: int = 50
) -> list:
    """List reminders with optional filtering."""
    
    script = '''
tell application "Reminders"
    tell list "openhands-bmad-agents"
        set remList to {}
        repeat with r in every reminder
            set remData to {id:id of r, name:name of r}
            if body of r is not missing value then
                set remData to remData & {body:body of r}
            end if
            if due date of r is not missing value then
                set remData to remData & {due_date:due date of r as text}
            end if
            if allday due date of r is not missing value then
                set remData to remData & {allday_due_date:allday due date of r as text}
            end if
            set remData to remData & {priority:priority of r, flagged:flagged of r, completed:completed of r}
            set end of remList to remData
        end repeat
        return remList
    end tell
end tell
'''
    
    output = run_applescript(script)
    if not output:
        return []
    
    # Parse the output - AppleScript returns POSIX arrays
    reminders = parse_applescript_list(output)
    
    # Apply filters
    filtered = []
    for r in reminders:
        # Filter by tags
        if filter_tags:
            body = r.get('body', '').lower()
            if not any(tag.lower() in body for tag in filter_tags):
                continue
        
        # Filter by flagged status
        if filter_flagged is not None:
            if r.get('flagged', False) != filter_flagged:
                continue
        
        # Filter by completed status
        if filter_completed == "completed" and not r.get('completed', False):
            continue
        elif filter_completed == "uncompleted" and r.get('completed', False):
            continue
        
        filtered.append(r)
        if len(filtered) >= limit:
            break
    
    return filtered


def parse_applescript_list(output: str) -> list:
    """Parse AppleScript list output to Python dicts."""
    # AppleScript format: {key1:value1, key2:value2, ...}
    results = []
    
    if not output or output == '{}':
        return []
    
    # Split by }{ for each dict
    items = output.split('},{')
    
    for item in items:
        item = item.strip('{} ')
        if not item:
            continue
        
        record = {}
        pairs = item.split(', ')
        
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip()
                # Parse value
                if value.startswith('{'):
                    # Nested list
                    continue
                elif value == 'true':
                    record[key] = True
                elif value == 'false':
                    record[key] = False
                elif value.isdigit():
                    record[key] = int(value)
                else:
                    record[key] = value.strip('" ')
        
        if record:
            results.append(record)
    
    return results


def get_reminder(reminder_id: str) -> dict:
    """Get single reminder by ID."""
    script = 'tell application "Reminders"\n'
    script += '    set r to reminder id "' + reminder_id + '"\n'
    script += '    set remData to {id:id of r, name:name of r}\n'
    script += '    if body of r is not missing value then\n'
    script += '        set remData to remData & {body:body of r}\n'
    script += '    end if\n'
    script += '    if due date of r is not missing value then\n'
    script += '        set remData to remData & {due_date:due date of r as text}\n'
    script += '    end if\n'
    script += '    set remData to remData & {priority:priority of r, flagged:flagged of r, completed:completed of r, creation_date:creation date of r as text, modification_date:modification date of r as text}\n'
    script += '    return remData\n'
    script += 'end tell'
    
    output = run_applescript(script)
    records = parse_applescript_list(output)
    return records[0] if records else {}


def update_reminder(
    reminder_id: str,
    name: Optional[str] = None,
    body: Optional[str] = None,
    due_date: Optional[str] = None,
    due_time: Optional[str] = None,
    priority: Optional[int] = None,
    flagged: Optional[bool] = None,
    completed: Optional[bool] = None
) -> dict:
    """Update an existing reminder."""
    
    script = 'tell application "Reminders"\n'
    script += '    set r to reminder id "' + reminder_id + '"\n'
    
    if name is not None:
        script += '    set name of r to "' + name.replace('"', '\\"') + '"\n'
    
    if body is not None:
        script += '    set body of r to "' + body.replace('"', '\\"') + '"\n'
    
    if due_date is not None:
        if due_time:
            script += '    set due date of r to date "' + due_date + ' ' + due_time + ':00"\n'
        else:
            script += '    set allday due date of r to date "' + due_date + '"\n'
    
    if priority is not None:
        script += '    set priority of r to ' + str(priority) + '\n'
    
    if flagged is not None:
        script += '    set flagged of r to ' + ('true' if flagged else 'false') + '\n'
    
    if completed is not None:
        script += '    set completed of r to ' + ('true' if completed else 'false') + '\n'
    
    script += 'end tell'
    
    run_applescript(script)
    return {"status": "updated", "id": reminder_id}


def delete_reminder(reminder_id: str) -> dict:
    """Delete a reminder."""
    script = f'''
tell application "Reminders"
    set r to reminder id "{reminder_id}"
    delete r
end tell
'''
    run_applescript(script)
    return {"status": "deleted", "id": reminder_id}


def main():
    parser = argparse.ArgumentParser(description='macOS Reminders CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new reminder')
    add_parser.add_argument('--name', required=True, help='Reminder title')
    add_parser.add_argument('--body', help='Description/body')
    add_parser.add_argument('--due-date', help='Due date YYYY-MM-DD')
    add_parser.add_argument('--due-time', help='Due time HH:MM')
    add_parser.add_argument('--priority', type=int, default=0, help='Priority 1-9, 0=none')
    add_parser.add_argument('--flagged', action='store_true', help='Mark as flagged')
    add_parser.add_argument('--tags', nargs='*', help='Tags as #hashtag')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List reminders')
    list_parser.add_argument('--filter-tags', nargs='*', help='Filter by tags')
    list_parser.add_argument('--filter-flagged', action='store_true')
    list_parser.add_argument('--filter-unflagged', action='store_true')
    list_parser.add_argument('--filter-completed', choices=['completed', 'uncompleted', 'all'], default='all')
    list_parser.add_argument('--limit', type=int, default=50)
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get reminder by ID')
    get_parser.add_argument('reminder_id', help='Reminder ID (x-apple-reminder://...)')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update reminder')
    update_parser.add_argument('reminder_id', help='Reminder ID')
    update_parser.add_argument('--name', help='New title')
    update_parser.add_argument('--body', help='New body')
    update_parser.add_argument('--due-date', help='New date YYYY-MM-DD')
    update_parser.add_argument('--due-time', help='New time HH:MM')
    update_parser.add_argument('--priority', type=int, help='New priority')
    update_parser.add_argument('--flagged', action='store_true')
    update_parser.add_argument('--unflagged', action='store_true')
    update_parser.add_argument('--completed', action='store_true')
    update_parser.add_argument('--uncompleted', action='store_true')
    
    # Delete command
    del_parser = subparsers.add_parser('delete', help='Delete reminder')
    del_parser.add_argument('reminder_id', help='Reminder ID')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'add':
            tags = args.tags if args.tags else None
            result = add_reminder(
                name=args.name,
                body=args.body,
                due_date=args.due_date,
                due_time=args.due_time,
                priority=args.priority,
                flagged=args.flagged,
                tags=tags
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == 'list':
            filter_flagged = None
            if args.filter_flagged:
                filter_flagged = True
            elif args.filter_unflagged:
                filter_flagged = False
            
            results = list_reminders(
                filter_tags=args.filter_tags,
                filter_flagged=filter_flagged,
                filter_completed=args.filter_completed,
                limit=args.limit
            )
            print(json.dumps(results, ensure_ascii=False, indent=2))
            
        elif args.command == 'get':
            result = get_reminder(args.reminder_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == 'update':
            flagged = None
            if args.flagged:
                flagged = True
            elif args.unflagged:
                flagged = False
            
            completed = None
            if args.completed:
                completed = True
            elif args.uncompleted:
                completed = False
            
            result = update_reminder(
                reminder_id=args.reminder_id,
                name=args.name,
                body=args.body,
                due_date=args.due_date,
                due_time=args.due_time,
                priority=args.priority,
                flagged=flagged,
                completed=completed
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
        elif args.command == 'delete':
            result = delete_reminder(args.reminder_id)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()