import json
import re

# has:
#  class code (ENC 1101)
#  department (GEHUM)
#  section (02)
#  name (English Comp. 1: Expository and Argumentative)
#  teacher name (C. Wylie / Lenz)
#  room (IST-1060)
#  days (TR)
#  time (12:30 - 1:45)

with open('courses.json') as f:
 courses = json.load(f)

import functools as ft, itertools as it,operator as op
ig = op.itemgetter
imap = map
map = lambda *args:list(imap(*args))

def p(*x):
 print(*x)

def pl(x):
 for i in x:
  print(i)

# parse the course id
courses = [list(re.fullmatch('([A-Z]{3})([0-9]{4}L?)(I&T|GENS|ENGR|GEENG|GEMTH|GEHUM|CENGR|CENG|CI&T|GESS|CGENS|GE)([0-9]{2}(?:HB)?|SP|IS)', c[0]).groups()+tuple(c[1:])) for c in courses]

for c in courses:
 startparts = re.fullmatch('([0-9]{1,2}):([0-9]{2}):00 (AM|PM)|TB/A',c[8]).groups()
 if startparts[0] != None:
  h = int(startparts[0]) + (12 if (startparts[2] == 'PM') ^ (startparts[0] == '12') else 0)
  m = int(startparts[1])
  start = f'{h:02d}{m:02d}'
  if start == '2400':
   start = ''
 else:
  start = '????'
 c[8] = start
 endparts = re.fullmatch('([0-9]{1,2}):([0-9]{2}):00 (AM|PM)|TB/A',c[9]).groups()
 if endparts[0] != None:
  h = int(endparts[0]) + (12 if (endparts[2] == 'PM') ^ (endparts[0] == '12') else 0)
  m = int(endparts[1])
  end = f'{h:02d}{m:02d}'
  if end == '2400':
   end = ''
 else:
  end = '????'
 c[9] = end
 if c[7] == 'N\\A':
  c[6] = ''
  c[7] = ''
 c[:2] = [c[0] + ' ' + c[1]]
 c[4:5] = reversed(c[4].split(', '))

courses = [{k:v for k,v in zip(['code', 'department', 'section', 'name', 'tfirst', 'tlast', 'room', 'days', 'start', 'end'], c)} for c in courses]