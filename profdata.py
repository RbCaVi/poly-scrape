import json

with open('profs.json') as f:
 profs = json.load(f)

#profs = __import__("profs").profs

def contains(s,e,v):
 return v >= s and v <= e

def overlap(s1,e1,s2,e2):
 return any([
  contains(s1,e1,s2),
  contains(s1,e1,e2),
  contains(s2,e2,s1),
  contains(s2,e2,e1),
 ])

# it's a database now!

classes = []
chours = []
phours = []
for i,p in enumerate(profs):
 p['id'] = i
 for j,cls in enumerate(p['classes']):
  cls['id'] = len(classes)
  cls['profid'] = i
  classes.append(cls)
  for day in cls['days']:
   chours.append((cls['id'],cls['room'],day,cls['start'],cls['end']))
 for day,hs in [*p['hours'].items()]:
  for h in hs:
   phours.append((i,day.upper(),h['start'],h['end']))
  p['hours'][day.upper()] = p['hours'][day]
  del p['hours'][day]

timetravel = set()
overlaps = set()
for h1 in chours:
 for h2 in chours:
  if h1 == h2:
   continue
  i1,r1,d1,s1,e1 = h1
  i2,r2,d2,s2,e2 = h2
  if r1 != r2 or d1 != d2:
   continue
  if overlap(int(s1),int(e1),int(s2),int(e2)):
   #print(h1,h2,'overlap',classes[i1]['code'],profs[classes[i1]['profid']]['room'],classes[i2]['code'],profs[classes[i2]['profid']]['room'])
   overlaps.add((i1,i2))

for h in chours:
 i,r,d,s,e = h
 if int(e) < int(s):
  timetravel.add(i)
 #print(h)

"""
profs = [prof]
prof = {
 'name': str
 'title': str
 'email': str
 'phone': str
 'room': room
 'classes': [class]
 'hours': hours
}
class = {
 'code': str
 'sec': str
 'days': [day]
 'start': time
 'end': time
 'room': room
}
"""