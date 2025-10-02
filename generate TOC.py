import re
import sys
import os
from collections import defaultdict

# Configurable Variables
DEFAULT_CSS_FILE = 'mal-midnight-blue.css'
TAB_SIZE = 2
TOC_FILE = 'toc.txt'
LINE_LEN = 80
OTHER_CONSTANTS_LEN = 7
TITLE_LEN = 19

# Reference Variables
no_of_equals = LINE_LEN + OTHER_CONSTANTS_LEN
no_of_spaces = int((no_of_equals - TITLE_LEN) / 2)

# Use filename from command-line argument if provided
css_file_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSS_FILE

# Check if file exists
if not os.path.exists(css_file_path):
  print(f"Error: File '{css_file_path}' not found.")
  sys.exit(1)

# Read CSS file line-by-line
with open(css_file_path, 'r', encoding='utf-8') as file:
  lines = file.readlines()

# Regex to match comment headers: /* 2.2.1 - Some Title */
pattern = re.compile(r'/\*[\s\-]*([\d.]+)\s*-\s*(.*?)\s*[\-]*\*/')

# Store matches with line numbers
entries = []
for idx, line in enumerate(lines, start=1):
  match = pattern.search(line)
  if match:
    number = match.group(1).strip()
    title = re.sub(r'[\s\-]+$', '', match.group(2).strip())  # clean trailing hyphens
    entries.append((number, title, idx))

# Group entries by their top-level section (e.g., "2.0.0")
grouped_entries = defaultdict(list)
for number, title, line_number in entries:
  parts = number.split('.')
  if len(parts) >= 2:
    section_key = f"{parts[0]}.0.0"
  else:
    section_key = number
  grouped_entries[section_key].append((number, title, line_number))

# Sort top-level sections
sorted_section_keys = sorted(grouped_entries.keys(), key=lambda x: list(map(int, x.split('.'))))


def get_indent_level(number):
  parts = list(map(int, number.split('.')))
  trailing_zeros = 0
  for p in reversed(parts):
    if p == 0:
      trailing_zeros += 1
    else:
      break
  indent_level = len(parts) - 1 - trailing_zeros
  return max(indent_level, 0)


# Build Table of Content
def build_toc(entries, section_keys, offset=0):
  toc_lines = [
    f"/* {'=' * no_of_equals} */",
    f"/* {' ' * no_of_spaces} TABLE OF CONTENTS {' ' * no_of_spaces} */",
    f"/* {'=' * no_of_equals} */"
  ]

  for i, section_key in enumerate(section_keys):
    group = sorted(entries[section_key], key=lambda x: list(map(int, x[0].split('.'))))

    if i > 0:
      toc_lines.append("")

    for number, title, line_number in group:
      indent_level = get_indent_level(number)
      indent = '\t' * indent_level if indent_level > 0 else ''
      label = f"{number} - {title}"
      label_len = len(label) + (indent_level * TAB_SIZE)
      adjusted_line = line_number + offset
      dots = '.' * (LINE_LEN - label_len - len(str(adjusted_line)))
      toc_lines.append(f"{indent}/* {label} {dots} line {adjusted_line} */")

  toc_lines.append(f"/* {'=' * no_of_equals} */")
  return toc_lines


# --- First pass (to get TOC size) ---
temp_toc = build_toc(grouped_entries, sorted_section_keys, offset=0)
toc_line_count = len(temp_toc)

# --- Second pass (apply offset) ---
toc_lines = build_toc(grouped_entries, sorted_section_keys, offset=toc_line_count)

# Output TOC to console (optional)
# print('\n'.join(toc_lines))

# Save TOC to a file
toc_output = '\n'.join(toc_lines)
with open(TOC_FILE, 'w', encoding='utf-8') as toc_file:
  toc_file.write(toc_output)

print(f"\nTOC saved to {TOC_FILE}")
