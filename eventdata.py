import json

with open('events.json') as f:
 events = json.load(f)

y,m,d = events['day']
del events['day']

import datetime
today = datetime.date(year = y, month = m, day = d)

'''
['StatusId', 'StatusTypeId', 'IsAllDayEvent', 'Id']
print()
for x in sorted({(e['Building'], e['BuildingId'], e['Location'], e['RoomId'], e['RoomType'], e['RoomTypeId'], e['RoomCode'], e['Room']) for e in events.values()}):
 print(x)

print()
for x in sorted({(e['Building'], e['BuildingId']) for e in events.values()}):
 print(x)

print()
for x in sorted({(e['RoomType'], e['RoomTypeId']) for e in events.values()}):
 print(x)

print()
for x in sorted({(e['Building'], e['BuildingId'], e['Location'], e['RoomId'], e['RoomCode'], e['Room']) for e in events.values()}):
 print(x)
'''
'''
def allunique(xss):
 l = len(xss)
 return all([len(set(xs)) == l for xs in zip(*xss)])
'''
b = lambda ks: {tuple(e[k] for k in ks) for e in events.values()}
'''
a = lambda ks: allunique(b(ks))
'''
import itertools as it
'''
kss = [sum(ks, []) for ks in it.product(*[[[], [k]] for k in next(iter(events.values())).keys()])]
kssm = {tuple(ks) for ks in kss if a(ks)}

print(len(kss), len(kssm))
top = [x for x in kssm if len({y for y in kssm if set(x).issubset(set(y)) and x != y}) == 0]
'''
'''
# the code above usually gives this result
top = [('Id',), ('Building', 'BuildingId'), ('EventEnd',), ('Location', 'Room', 'RoomCode', 'RoomId'), ('StatusTypeId',), ('RoomTypeId', 'RoomType'), ('StatusId',), ('IsAllDayEvent',), ('EventName',), ('GroupName',), ('EventStart',)]

c = lambda ks1, ks2: len(b(ks1)) == len(b(ks1 + ks2))

deps = sorted((ks1, ks2) for ks1 in top for ks2 in top if c(ks1, ks2) and ks1 != ks2)

depis = [(top.index(ks1), top.index(ks2)) for ks1,ks2 in deps]
for _ in range(len(deps)):
 depis = [i12 for i12 in depis if i12 not in [(i1,i4) for i1,i2 in depis for i3,i4 in depis if i2 == i3]]

for i1,i2 in depis:
 print(f'{top[i1]},{len(b(top[i1]))}>{top[i2]},{len(b(top[i2]))}')
'''
events = [{**e, 'id': i} for i,e in enumerate(events.values())]

cevents = [e for e in events if e['GroupName'] == 'Registrar']

import re
def extracttime(t):
 time = re.match(f'{y:04}-{m:02}-{d:02}T'r'(\d\d):(\d\d):00', t).groups()
 return time[0] + time[1]

eclasses = []
for i,c in enumerate(cevents):
 dep,num,sec,name = re.fullmatch(r'(?:(.{3})-(\d{4}(?:C|L|))-(\d{2}(?:HB)?) )?(.*)', c['EventName']).groups()
 name = name.replace('&amp;', '&')
 #print(dep, num, sec, name, c['Room'], extracttime(c['EventStart']), extracttime(c['EventEnd']))
 eclasses.append({
  'id': i,
  'code': f'{dep} {num}' if dep is not None else '',
  'section': sec,
  'name': name,
  'room': c['Room'],
  'start': extracttime(c['EventStart']),
  'end': extracttime(c['EventEnd']),
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