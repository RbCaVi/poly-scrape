import json

# matches classes from ems to the merged database i made
# for some reason, results in different counts of matched classes every time i run it

with open('events.json') as f:
 events = json.load(f)

y,m,d = events['day']
del events['day']

import datetime
today = datetime.date(year = y, month = m, day = d)

import itertools as it

cevents = [e for e in events['events'] if e['owner'] == 'Registrar']

import re

eclasses = []
for i,c in enumerate(cevents):
 dep,num,sec,name = re.fullmatch(r'(?:(.{3})-(\d{4}(?:C|L|))-(\d{2}(?:HB)?) )?(.*)', c['name']).groups()
 name = name.replace('&amp;', '&')
 eclasses.append({
  'id': i,
  'code': f'{dep} {num}' if dep is not None else '',
  'section': sec,
  'name': name,
  'room': c['room'],
  'start': c['start'],
  'end': c['end'],
 })

day = 'MTWRF__'[today.weekday()]

import polydata

pclasses = [c for c in polydata.mergedclasses if day in (c['days'] or '')]

ecodes = sorted([c['code'] for c in eclasses])
pcodes = sorted([c['code'] for c in pclasses])

print(ecodes)
print(pcodes)

print(sorted(set(ecodes) - set(pcodes)))
print(sorted(set(pcodes) - set(ecodes)))

pairs = []
for (ie,ec),(ip,pc) in it.product(enumerate(eclasses), enumerate(pclasses)):
 if ec['code'] != pc['code']:
  continue
 if ec['section'] != pc['section']:
  continue
 if ec['start'] != pc['start']:
  continue
 if ec['end'] != pc['end']:
  continue
 if ec['room'] != pc['room']:
  print(ec['room'], '!=', pc['room'], '!!!!!')
 pairs.append((ie, ip))

assert len(pairs) == len([p[0] for p in pairs]), 'doubled class event'
assert len(pairs) == len([p[0] for p in pairs]), 'doubled poly class (cams / office)'
print(len(pairs), 'matched classes')