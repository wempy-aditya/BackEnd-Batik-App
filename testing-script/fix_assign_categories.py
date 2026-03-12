"""
Temporary script to fix assign_categories method
"""

# Mari baca assign_categories method yang ada dan buat versi baru
import re

with open('/home/wempy/fastapi_project/fastapi-boilerplate/src/app/crud/crud_publications.py', 'r') as f:
    content = f.read()

# Count how many assign_categories methods exist
count = content.count('async def assign_categories(')
print(f"Found {count} assign_categories methods")

# Find all methods
pattern = r'async def assign_categories\([^}]*?\n        return updated_publication'
matches = re.findall(pattern, content, re.DOTALL)

print(f"Found {len(matches)} full methods")
for i, match in enumerate(matches):
    print(f"\n=== Method {i+1} ===")
    print(match[:200] + "...")