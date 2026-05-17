# macOS Reminders Integration

Integrates with native macOS Reminders app via AppleScript to manage tasks in the "openhands-bmad-agents" list.

## Operations

### add_reminder
Creates a new reminder with all supported parameters.

**Parameters:**
- `name` (required): Title of the reminder (max 255 chars)
- `body` (optional): Detailed description or notes
- `due_date` (optional): Date in format YYYY-MM-DD
- `due_time` (optional): Time in format HH:MM (24h)
- `priority` (optional): 1=high, 5=medium, 9=low, 0=none
- `flagged` (optional): true/false for flag marking
- `tags` (optional): Array of tags (stored as #hashtag in body)

**Example:**
```
add_reminder(
  name="Scrapowanie ofert z LinkedIn",
  body="Przetestować scraper LinkedIn dla ML Engineer",
  due_date="2026-05-20",
  due_time="09:00",
  priority=1,
  tags=["agent-rekrut", "scraper", "priority-high"]
)
```

### list_reminders
Lists all reminders with optional filtering.

**Parameters:**
- `filter_tags` (optional): Show only reminders containing these tags
- `filter_flagged` (optional): true=only flagged, false=only unflagged
- `filter_completed` (optional): true=completed, false=uncompleted, "all"=all
- `limit` (optional): Max number of results (default 50)

**Returns:** Array of reminder objects with id, name, body, due date, priority, flagged, completed status.

### get_reminder
Gets detailed information about a specific reminder.

**Parameters:**
- `reminder_id` (required): The reminder ID (x-apple-reminder://...)

### update_reminder
Modifies an existing reminder.

**Parameters:**
- `reminder_id` (required): The reminder ID
- `name` (optional): New title
- `body` (optional): New description
- `due_date` (optional): New date YYYY-MM-DD
- `due_time` (optional): New time HH:MM
- `priority` (optional): New priority (1/5/9/0)
- `flagged` (optional): true/false
- `completed` (optional): true/false

### delete_reminder
Removes a reminder from the list.

**Parameters:**
- `reminder_id` (required): The reminder ID

## Implementation Details

Uses `osascript` for AppleScript execution. Tags are implemented as #hashtags in body for compatibility with native Reminders.

## Notes

- Reminders app must be accessible (not encrypted with Screen Time restrictions)
- All times are in local system timezone
- ID format: x-apple-reminder://UUID
- Priority: 1=High, 5=Medium, 9=Low, 0=None

## CLI Usage

The skill also provides a CLI tool for direct execution:

```bash
# Add reminder
python3 .agents/skills/bmad-macos-reminders/macos-reminders.py add \
  --name "Tytuł zadania" \
  --body "Opis #tag" \
  --due-date 2026-05-20 \
  --priority 5 \
  --flagged \
  --tags project agent

# List with filters
python3 .agents/skills/bmad-macos-reminders/macos-reminders.py list \
  --filter-tags agent \
  --filter-completed uncompleted \
  --limit 20

# Get details
python3 .agents/skills/bmad-macos-reminders/macos-reminders.py get "x-apple-reminder://UUID"

# Update
python3 .agents/skills/bmad-macos-reminders/macos-reminders.py update "ID" --completed --priority 1

# Delete
python3 .agents/skills/bmad-macos-reminders/macos-reminders.py delete "x-apple-reminder://UUID"
```

## Example: Full Workflow

```python
import subprocess, json

def create_task(title, tags):
    """Create task in Reminders."""
    cmd = [
        'python3', 
        '.agents/skills/bmad-macos-reminders/macos-reminders.py',
        'add', '--name', title, '--tags'
    ] + tags
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

def get_active_tasks(tag_filter):
    """Get uncompleted tasks with tag."""
    result = subprocess.run(
        ['python3', '.agents/skills/bmad-macos-reminders/macos-reminders.py', 
         'list', '--filter-tags', tag_filter, '--filter-completed', 'uncompleted'],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def complete_task(reminder_id):
    """Mark task as completed."""
    subprocess.run(
        ['python3', '.agents/skills/bmad-macos-reminders/macos-reminders.py',
         'update', reminder_id, '--completed'],
        capture_output=True
    )
```