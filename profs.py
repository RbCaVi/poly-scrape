# the professor data is copied down off the papers on the office doors
# the only data this gives over cams and directory is the office hours
# i typed it all out myself :(
# i made a few minor corrections like course numbers
# it has for each professor:
#   name (usually exactly as shown on the door paper)
#   title (professor or department chair etc)
#   email & phone
#   room - the actual room, not the one on the paper
#   department
#   classes
#     code (MAC 2312) & section
#     days of the week and time (as 4 digit 24 hr string because i was lazy)
#     the room it is held in
#   office hours
#     day and start / end (4 digit 24 hr)
with open('fl poly professors data - fall 2024.txt') as f:
 lines = [line.split('#')[0].split(';') for line in f.read().strip().split('\n')]

#print(lines)
#print([len(line) for line in lines])

departments = {"cs":"Computer Science", "ph":"Physics", "am":"Applied Mathematics", "ee":"Environmental Engineering","phc":"Physics","dsba":"Data Science and Business Analytics","na":"","ahs":"Arts, Humanities, and Social Sciences","ce":"Civil Engineering","miecec":"Mechanical, Industrial, Environmental and Civil Engineering","me":"Mechanical Engineering","ie":"Industrial Engineering"}
proflines = [i for i,line in enumerate(lines) if len(line)==6 and line[0] in departments]

profs = []
for i,i2 in zip(proflines,proflines[1:]+[len(lines)]):
 entry = {}
 prof,*data = lines[i:i2]
 dep,name,title,email,phone,room = prof
 dep = dep
 name = name.title()
 title = title.title()
 email = email + '@floridapoly.edu' if email != '' else ''
 phone = '863-874-' + phone if phone != '' else ''
 room = room.upper()
 entry['name'] = name
 entry['title'] = title
 entry['email'] = email
 entry['phone'] = phone
 entry['room'] = room
 entry['department'] = departments[dep]
 classes = [line for line in data if len(line) == 6]
 hours = [line for line in data if len(line) == 3]
 other = [line for line in data if len(line) == 3 and len(line) == 6 and line != ['']]
 for o in other:
   print('nope:', o)
 entryclasses = []
 for uclass in classes:
  centry = {}
  code,sec,days,start,end,room = uclass
  code = code.upper()
  days = list(days.upper())
  room = room.upper()
  if len(code) < 8:
    print("nope:",code)
  centry['code'] = code
  centry['sec'] = sec
  centry['days'] = days
  centry['start'] = start
  centry['end'] = end
  centry['room'] = room
  entryclasses.append(centry)
 entry['classes'] = entryclasses
 hoursbyday = {day:[] for day in 'mtwrf'}
 appointment = False
 for days,start,end in hours:
  for day in days:
   if days == 'a':
    appointment = True
    continue
   hoursbyday[day].append({'start': start,'end': end})
 entry['hours'] = hoursbyday
 profs.append(entry)

import json
with open('profs.json', 'w') as f:
 json.dump(profs, f)