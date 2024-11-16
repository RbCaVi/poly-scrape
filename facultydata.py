import json
import re

with open('faculty.json') as f:
 faculty = json.load(f)

for i,p in enumerate(faculty):
 p['id'] = i