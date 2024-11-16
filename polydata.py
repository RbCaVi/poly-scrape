import json
import re

# merges three sources into a table of professors and a table of classes
# sources are fl poly directory (faculty), cams (courses), and professor office door papers (profs)
# some fields may be None if there is no matching entry in one of the sources
# professors (mergedprofs):
#  id (the index into the table)
#  email and phone
#  room
#  department
#  two names - faculty / office door and teacher
#  two titles - faculty and office door
#  office hours - dict of day (MTWRF) to list of segments {"start": "1100", "end": "1200"}
#  type and campus - directly from faculty
# classes / courses (mergedclasses):
#  id
#  code and section (MAC 2312 / 03)
#  days (MTWF)
#  time (11:00 - 11:50)
#  room
#  department - from cams
#  name - also from cams
#  teacher - id in mergedprofs

import functools as ft, itertools as it,operator as op
ig = op.itemgetter
b = ft.partial
imap = map
map = lambda *args: list(imap(*args))
izip = zip
zip = lambda *args: list(izip(*args))
ifilter = filter
filter = lambda *args: list(ifilter(*args))

def p(*x):
 pass#print(*x)

def pl(x):
 for i in x:
  pass#print(i)

def a1(l):
 assert len(l) == 1
 return l[0]

def aset(d, k, v):
 assert d.get(k, v) == v
 d[k] = v

from profdata import profs, classes
from coursedata import courses
from facultydata import faculty

#pl(map(ig('name','title'), profs))
m = lambda f: lambda l: map(f, l)
tm = lambda *fs: lambda xs: [f(x) for f,x in zip(fs, xs)]
grp = lambda kf, xs: [(k, [x for x in xs if kf(x) == k]) for k in {kf(x) for x in xs}]
eq = lambda v1: lambda v2: v1 == v2
on = lambda i, f: lambda x: f(x[i])
ap = lambda f: lambda *fs: lambda x: f(*(f(x) for f in fs))
i = lambda x: x
pr = lambda l1, l2: [*it.product(l1, l2)]
tup = lambda *xs: tuple(xs)

fprofs = filter(on('type', eq('faculty')), faculty)
roomless = filter(on('room', eq('')), faculty)

teachers = [{'id': i, 'tfirst': t[0], 'tlast': t[1]} for i,t in enumerate((set(map(ig('tfirst', 'tlast'), courses))))]
for i,course in enumerate(courses):
 course['id'] = i
 course['tid'] = a1([t for t in teachers if t['tfirst'] == course['tfirst'] and t['tlast'] == course['tlast']])['id']

tnames = map(ig('tfirst', 'tlast'), teachers)
pnames = map(ig('name'), profs)

matches = filter(lambda x: x[1][0] in x[0] and x[1][1] in x[0], pr(pnames, tnames))
ptmatches = [(p, len([t for t in tnames if t[0].lower() in p.lower() and t[1].lower() in p.lower()])) for p in pnames]
tpmatches = [(t, len([p for p in pnames if t[0].lower() in p.lower() and t[1].lower() in p.lower()])) for t in tnames]
# there are no double matches
punmatched = sorted(filter(on(1, b(op.ne, 1)), ptmatches))
tunmatched = sorted(filter(on(1, b(op.ne, 1)), tpmatches))



mapping = {}
for p,t in matches:
 pi = a1([prof['id'] for prof in profs if prof['name'] == p])
 ti = a1([teacher['id'] for teacher in teachers if (teacher['tfirst'], teacher['tlast']) == t])
 aset(mapping, pi, ti)

ptum = {name:a1([prof['id'] for prof in profs if prof['name'] == name]) for name,_ in punmatched}
tpum = {name:a1([teacher['id'] for teacher in teachers if (teacher['tfirst'], teacher['tlast']) == name]) for name,_ in tunmatched}

def m(a, b):
 aset(mapping, ptum[a], tpum[b])
 del ptum[a]
 del tpum[b]

m('Dr. Ala Alnaser, Ph.D.', ("Ala' Jamil", 'Alnaser'))
m('Dr. Gerardo Carbajal', ('Gerardo J', 'Carbajal'))
m('Dr. James Dewey', ('Jim', 'Dewey'))
m('Dr. Lorraine Laguerre', ('Lorraine', 'Laguerre Van Sickle'))
m('Dr. Satyajith (Sj) Boyana, Ph.D', ('Satyajith', 'Bommana Boyana'))

fnames = map(ig('name'), faculty) # fprofs?

fmatches = filter(lambda x: x[1].lower() in x[0].lower(), pr(pnames, fnames))
pfmatches = [(p, len([f for f in fnames if f.lower() in p.lower()])) for p in pnames]
fpmatches = [(f, len([p for p in pnames if f.lower() in p.lower()])) for f in fnames]
pfunmatched = sorted(filter(on(1, b(op.ne, 1)), pfmatches))
fpunmatched = sorted(filter(on(1, b(op.ne, 1)), fpmatches))

pfum = {name:a1([prof['id'] for prof in profs if prof['name'] == name]) for name,_ in pfunmatched}
fpum = {name:a1([prof['id'] for prof in faculty if prof['name'] == name]) for name,_ in fpunmatched}

mapping2 = {}
for p,f in fmatches:
 pi = a1([prof['id'] for prof in profs if prof['name'] == p])
 fi = a1([prof['id'] for prof in faculty if prof['name'] == f])
 aset(mapping2, pi, fi)

def m2(a, b):
 aset(mapping2, pfum[a], fpum[b])
 del pfum[a]
 del fpum[b]

m2('Dr. Ayesha S. Dina', 'Ayesha Dina')
m2('Dr. C. Wylie. Lenz, Ph.D.', 'C. Wylie Lenz')
m2('Dr. Lorraine Laguerre', 'Lorraine Laguerre Van Sickle')
m2('Dr. Manoj Sargunaraj', 'Manoj Prabakar Sargunaraj')
m2('Dr. Pedro Manrique', 'Pedro Manrique Charry')
m2('Dr. Sanjeeta Ghimire', 'Sanjeeta N. Ghimire')
m2('Dr. Sathish Akula', 'Sathish Chandra Akula')
m2('Dr. Xiaofan "Caleb" Xu', 'Xiaofan Xu')


tmatches = filter(lambda x: x[1][0] in x[0] and x[1][1] in x[0], pr(fnames, tnames))
ftmatches = [(p, len([t for t in tnames if t[0].lower() in p.lower() and t[1].lower() in p.lower()])) for p in fnames]
tfmatches = [(t, len([p for p in fnames if t[0].lower() in p.lower() and t[1].lower() in p.lower()])) for t in tnames]
# there are no double matches
ftunmatched = sorted(filter(on(1, b(op.ne, 1)), ftmatches))
tfunmatched = sorted(filter(on(1, b(op.ne, 1)), tfmatches))

mapping3 = {}
for f,t in tmatches:
 fi = a1([prof['id'] for prof in faculty if prof['name'] == f])
 ti = a1([teacher['id'] for teacher in teachers if (teacher['tfirst'], teacher['tlast']) == t])
 aset(mapping3, fi, ti)

ftum = {name:a1([prof['id'] for prof in faculty if prof['name'] == name]) for name,_ in ftunmatched}
tfum = {name:a1([teacher['id'] for teacher in teachers if (teacher['tfirst'], teacher['tlast']) == name]) for name,_ in tfunmatched}

def m3(a, b):
 aset(mapping3, ftum[a], tfum[b])
 del ftum[a]
 del tfum[b]

m3('Ala Alnaser', ("Ala' Jamil", 'Alnaser'))
m3('Bradford Towle', ('Bradford', 'Towle Jr.'))
m3('Gerardo Carbajal', ('Gerardo J', 'Carbajal'))
m3('James Dewey', ('Jim', 'Dewey'))
m3('Satyajith (SJ) Boyana', ('Satyajith', 'Bommana Boyana'))
m3('Debbie Frank', ('Debra', 'Frank'))

mapping
mapping2
mapping3

def outerjoin(a, b, i1, i2):
 out = set()
 m1 = set()
 m2 = set()
 for v1,v2 in pr(a,b):
  if v1[i1] == v2[i2]:
   m1.add(v1)
   m2.add(v2)
   out.discard(v1 + (None,) * len(v2))
   out.discard((None,) * len(v1) + v2)
   out.add(v1 + v2)
  if v1 not in m1:
   out.add(v1 + (None,) * len(v2))
  if v2 not in m2:
   out.add((None,) * len(v1) + v2)
 return out

total = outerjoin(outerjoin(mapping.items(),mapping2.items(),0,0),mapping3.items(),3,0)

def coalesce(a, b):
 if a is None:
  return b
 if b is None:
  return a
 assert a == b
 return a

tot = []
for p1,t1,p2,f1,f2,t2 in total:
 tot.append((coalesce(p1, p2), coalesce(t1, t2), coalesce(f1, f2)))

for p in [p['id'] for p in profs if p['id'] not in [e[0] for e in tot]]:
 tot.append((p, None, None))
for t in [t['id'] for t in teachers if t['id'] not in [e[1] for e in tot]]:
 tot.append((None, t, None))
#for f in [f['id'] for f in faculty if f['id'] not in [e[2] for e in tot]]:
# tot.append((None, None, f))

'''
# the entries have three ids which double as indexes into the three data tables - profs, teachers, faculty
print("PROFESSORS:\n")
for p,t,f in tot:
 print(p, t, f)
 if p is not None:
  print(' ', profs[p]['name'])
 else:
  print(' ', 'NO OFFICE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
 if t is not None:
  print(' ', teachers[t]['tfirst'], teachers[t]['tlast'])
 else:
  print(' ', 'NO CLASSES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
 if f is not None:
  print(' ', faculty[f]['name'])
 else:
  print(' ', 'NO DIRECTORY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
'''
'''
print()
print()
print()

print("professors in offices that aren't teaching a class", ptum)
print("professors teaching without an office", tpum)
print("office professors not faculty members", pfum)
print("faculty members without an office", {k:fpum[k] for k in fpum if k in [p['name'] for p in fprofs]})
print("faculty members not teaching this semester", {k:ftum[k] for k in ftum if k in [p['name'] for p in fprofs]})
print("teachers that aren't faculty", tfum)
'''
cmapping = []

for p,t,f in sorted(tot, key = lambda x: (x[0] or -1, x[1] or -1, x[2] or -1)):
 if p is not None and t is not None:
  #print(p, t)
  
  pclasses = profs[p]['classes']
  tclasses = [c for c in courses if c['tid'] == t]
  #print('pc')
  #for pc in pclasses:
  # print(pc['code'], pc['sec'], pc['start'], pc['end'], pc['room'])
  #print('tc')
  #for tc in tclasses:
  # print(tc['code'], tc['section'], tc['start'], tc['end'], tc['room'])
  pairs = []
  for i1,pc in enumerate(pclasses):
   for i2,tc in enumerate(tclasses):
    if pc['code'] != tc['code'] and pc['code'] != tc['code'] + 'C':
     continue
    if pc['start'] != tc['start']:
     continue
    if pc['end'] != tc['end']:
     continue
    if pc['room'] != tc['room']:
     continue
    if sorted(pc['days']) != sorted(tc['days']):
     continue
    if pc['sec'] not in tc['section']:
     pass
    pairs.append((i1, i2))
  i1s = [i for i,_ in enumerate(pclasses)]
  i2s = [i for i,_ in enumerate(tclasses)]
  m1 = [(i1, [p for p in pairs if p[0] == i1]) for i1 in i1s]
  m2 = [(i2, [p for p in pairs if p[1] == i2]) for i2 in i2s]
  for i1,i2 in pairs:
   cmapping.append((pclasses[i1]['id'], tclasses[i2]['id']))
  if len([m for m in m1 if len(m[1]) != 1]) > 0 or len([m for m in m2 if len(m[1]) != 1]) > 0:
   print(p, t)
   print(sorted(pairs))
   #print(profs[p]['name'])
   #print('pc')
   for i1,m in [m for m in m1 if len(m[1]) != 1]:
    pc = pclasses[i1]
    #print(i1, pc['code'], pc['sec'], pc['start'], pc['end'], pc['room'], sorted(pc['days']))
    assert len(m) == 0
    cmapping.append((pclasses[i1]['id'], None))
   #print('tc')
   for i2,m in [m for m in m2 if len(m[1]) != 1]:
    tc = tclasses[i2]
    #print(i2, tc['code'], tc['section'], tc['start'], tc['end'], tc['room'], sorted(tc['days']))
    assert len(m) == 0
    cmapping.append((None, tclasses[i2]['tid']))
   #print()

def getif(i, l):
 if i is None:
  return {}
 return l[i]

def coalesce2(a, b):
 if a == '':
  a = None
 if b == '':
  b = None
 return coalesce(a, b)

def coalesce3(a, b):
 if a == '':
  a = None
 if b == '':
  b = None
 if a is None:
  return b
 if b is None:
  return a
 if a != b:
  pass#print(a, "does not match", b, "!!!!!")
 return a

othermatches = {
 ("Arts, Humanities and Social Sciences", "Arts, Humanities, and Social Sciences"),
 ("Civil and Environmental Engineering", "Environmental Engineering"),
 ("Civil and Environmental Engineering", "Civil Engineering"),
 ("Business Analytics, Data Science", "Data Science and Business Analytics"),
}

def coalesce4(a, b):
 if a == '':
  a = None
 if b == '':
  b = None
 if a is None:
  return b
 if b is None:
  return a
 if a != b and (a, b) not in othermatches:
  pass#print(a, "does not match", b, "!!!!!")
 return a

mergedprofs = []
for p,t,f in tot:
 prof = getif(p, profs)
 teacher = getif(t, teachers)
 member = getif(f, faculty)
 out = {
  "id": len(mergedprofs),
  "email": coalesce2(prof.get('email'), member.get('email')),
  "phone": coalesce2(prof.get('phone'), member.get('phone')),
  "room": coalesce3(prof.get('room'), member.get('room')),
  "department": coalesce4(member.get('department'), prof.get('department')),
  "name": prof.get('name'),
  "first": teacher.get('tfirst'),
  "last": teacher.get('tlast'),
  "fname": member.get('name'),
  "title1": prof.get('title'),
  "title2": member.get('title'),
  "officehours": prof.get('hours'),
  "type": member.get('type'),
  "campus": member.get('campus'),
 }
 prof['mergedid'] = out['id']
 teacher['mergedid'] = out['id']
 member['mergedid'] = out['id']
 mergedprofs.append(out)

def coalescecode(a, b):
 if b is None:
  return a
 if b + 'C' == a:
  b = b + 'C'
 return coalesce2(a, b)

def coalescesec(a, b):
 if a is None:
  return b
 if b is None:
  return a
 if '0' * (len(b) - len(a)) + a == b:
  a = '0' * (len(b) - len(a)) + a
 return coalesce2(a, b)

mergedclasses = []
for oc,cc in sorted(cmapping, key = lambda x: (x[0] or -1, x[1] or -1)):
 oc = getif(oc, classes)
 cc = getif(cc, courses)
 if 'profid' in oc:
  tid = profs[oc['profid']]['mergedid']
 else:
  tid = teachers[cc['tid']]['mergedid']
 out = {
  "id": len(mergedclasses),
  "code": coalescecode(oc.get('code'), cc.get('code')),
  "section": coalescesec(oc.get('sec'), cc.get('section')),
  "days": coalesce2(''.join(oc.get('days') if 'days' in oc else []), cc.get('days')),
  "start": coalesce2(oc.get('start'), cc.get('start')),
  "end": coalesce2(oc.get('end'), cc.get('end')),
  "room": coalesce2(oc.get('room'), cc.get('room')),
  "department": cc.get('department'),
  "name": cc.get('name'),
  "teacher": tid,
 }
 oc['mergedid'] = out['id']
 cc['mergedid'] = out['id']
 mergedclasses.append(out)

data = {
 "classes": mergedclasses,
 "professors": mergedprofs,
}

print(len(mergedclasses), len(mergedprofs))
print(sorted([p['name'] for p in mergedprofs], key = lambda x: x if x is not None else ''))
print(sorted(set([c['code'] for c in mergedclasses]), key = lambda x: (x[8:], x) if x is not None else ('', '')))

def dumpj(file, data):
 with open(file, 'w') as f:
  json.dump(data, f)

dumpj('codes.json', sorted(set([c['code'] for c in mergedclasses]), key = lambda x: (x[8:], x) if x is not None else ('', '')))

with open('polydata.json', 'w') as f:
 json.dump(data, f)