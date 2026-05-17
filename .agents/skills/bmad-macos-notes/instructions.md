# macOS Notes Skill - Instructions

Native Apple Notes integration via macOS scripting.

## Operations

### list
List all notes in the folder.
```bash
python3 macos-notes.py list [--folder NAME] [--filter-tags TAG1 TAG2] [--limit N]
```
- `--filter-tags`: Show only notes containing specified hashtags
- `--limit`: Maximum number of notes (default: 50)

### get
Get a specific note by ID.
```bash
python3 macos-notes.py get <note-id>
```

### add
Create a new note.
```bash
python3 macos-notes.py add --name "Title" --body "Content #tag1 #tag2" [--tags tag1 tag2]
```

### update
Update a note's name, body, or add tags.
```bash
python3 macos-notes.py update <note-id> [--name "New Title"] [--body "New content"] [--add-tags tag1]
```

### delete
Delete a note.
```bash
python3 macos-notes.py delete <note-id>
```

### search
Search notes by name or content.
```bash
python3 macos-notes.py search "query" [--folder NAME]
```

## Notes on Tags

- Tags are stored in note body as `#tagname` (hashtags)
- Tags can be added automatically via `--tags` flag or appended with `--add-tags`
- Filtering by tag uses `--filter-tags` which searches body for `#tagname`

## Folder

Default folder: `openhands-bmad-agents`

Create this folder manually in Apple Notes first, or the skill will return empty results until the folder exists.