# scrape the fl poly directory for everything i guess
#   type (staff or faculty)
#   name & title
#   department
#   email & phone
#   campus - either "fl poly south" (polk state college - lakeland technology building?), main campus, fipr (florida industrial phosphate research institute), or none (no office i guess)
#   room

import requests
import bs4
import re

data = bs4.BeautifulSoup(requests.get('https://floridapoly.edu/directory/index.php').text, features="html.parser")

faculty = []
for p in data.select('tr')[1:]:
 typ = p['data-type']
 name = p.select_one('td h2').text.strip()
 title = p.select_one('td strong').text.strip()
 prefix = {'staff': 'Staff | ', 'faculty': 'Faculty | '}[typ]
 assert title.startswith(prefix)
 title = title[len(prefix):]
 dep = p.select_one('td.select').text.strip()
 assert dep == p.select_one('td.select')['data-search']
 email = p.select('td')[2].select_one('a').text.strip()
 assert 'mailto:' + email == p.select('td')[2].select_one('a')['href']
 phone = p.select('td')[3].select_one('a').text.strip()
 phone2 = p.select('td')[3].select_one('a')['href']
 if phone != '':
  assert re.fullmatch(r'\d{3}-\d{3}-\d{4}', phone) is not None
  assert re.fullmatch(r'tel:\+1\(\d{3}\)\d{7}', phone2) is not None
  assert re.fullmatch(r'(\d{3})-(\d{3})-(\d{4})', phone).groups() == re.fullmatch(r'tel:\+1\((\d{3})\)(\d{3})(\d{4})', phone2).groups()
 campus = p.select('td')[4].text.strip()
 room = p.select('td')[5].text.strip()
 faculty.append({
  'type': typ,
  'name': name,
  'title': title,
  'department': dep,
  'email': email,
  'phone': phone,
  'campus': campus,
  'room': room,
 })

a=[(y,[(x['name'],x['type']) for x in faculty if x['room'] == y]) for y in {x[1] for x in {(len(tuple(x['name'] for x in faculty if x['room'] == y)),y) for y in {x['room'] for x in faculty}} if x[0] != 1}]
for x in a:
 #print(x[0])
 for y in x[1]:
  pass#print(' ', y[1], y[0])

#print()
#print()
#print()

a=[(y,[(x['name'],x['type']) for x in faculty if x['room'] == y]) for y in {x[1] for x in {(len(tuple(x['name'] for x in faculty if x['room'] == y)),y) for y in {x['room'] for x in faculty}}}]
for x in a:
 #print(x[0])
 for y in x[1]:
  pass#print(' ', y[1], y[0])

a = sorted([r for r in {x['room'] for x in faculty} if not re.match('IST-|BARC-|LTB-', r)])	
#print(a)
'''
type
name
title
department
email
phone
campus
room
'''

import json
with open('faculty.json', 'w') as f:
 json.dump(faculty, f)