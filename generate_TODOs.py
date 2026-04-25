import re
import sys
import os

# Configurable Variables
DEFAULT_CSS_FILE = 'mal-midnight-blue.user.css'
TODO_FILE = 'todos.txt'
LINE_LEN = 80
OTHER_CONSTANTS_LEN = 7
TITLE_TODO = 'TODO LIST'

# Reference Variables
no_of_equals = LINE_LEN + OTHER_CONSTANTS_LEN
no_of_spaces_todo = int((no_of_equals - len(TITLE_TODO)))

# Use filename from command-line argument if provided
css_file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSS_FILE

# Check if file exists
if not os.path.exists(css_file_path):
  print(f"Error: File '{css_file_path}' not found.")
  sys.exit(1)

# Read CSS file line-by-line
with open(css_file_path, 'r', encoding='utf-8') as file:
  lines = file.readlines()

# Regex to match TODO comments: /* TODO: ... */
todo_pattern = re.compile(r'/\*\s*TODO:\s*(.*?)\s*\*/', re.IGNORECASE)

# Store TODO matches with line numbers
todos = []

for idx, line in enumerate(lines, start=1):
  todo_match = todo_pattern.search(line)
  if todo_match:
    todo_text = todo_match.group(1).strip()
    todos.append((todo_text, idx))

# Build TODO list
def build_todo_list(todos):
  if not todos:
    return ["/* No TODOs found */"]
  
  todo_lines = [
    f"/* {'=' * no_of_equals} */",
    f"/* {TITLE_TODO}{' ' * no_of_spaces_todo} */",
    f"/* {'=' * no_of_equals} */",
    ""
  ]
  
  for todo_text, line_number in todos:
    todo_lines.append(f"/* Line {line_number}: TODO: {todo_text} */")
  
  # Calculate spacing for the total line
  total_text = f"Total TODOs: {len(todos)}"
  total_text_len = len(total_text)
  spaces_needed = no_of_equals - total_text_len
  
  todo_lines.append("")
  todo_lines.append(f"/* {'=' * no_of_equals} */")
  todo_lines.append(f"/* {total_text}{' ' * spaces_needed} */")
  todo_lines.append(f"/* {'=' * no_of_equals} */")
  
  return todo_lines

# Generate TODO list
todo_lines = build_todo_list(todos)
todo_output = '\n'.join(todo_lines)

# Save TODO list to a file
with open(TODO_FILE, 'w', encoding='utf-8') as todo_file:
  todo_file.write(todo_output)

print(f"TODO list saved to {TODO_FILE} ({len(todos)} items found)")

# Output TODO to console (optional)
# print(todo_output)
