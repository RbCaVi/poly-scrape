import bs4
import requests
import re

# this is a term name from cams
term = 'FA 2024'

# put your username and password in creds.txt separated by some whitespace (space or newline would work)
with open('creds.txt') as f:
 u,pw = f.read().split()

def a1(l):
 assert len(l) == 1
 return l[0]

# cams needs authentication so uhhhhhh
# you need to copy the cookie (just the one here - AzureAppProxyAccessCookie) after you log into cams
# it's easy to do in chrome web tools - go to network - click on the first item at the top (usually) and copy the cookie

cookies = {"AzureAppProxyAccessCookie_019af695-0b74-4c2f-b822-02be1f8b5e6f_1.3": "MGD:MIICrAYJKoZIhvcNAQcDoIICnTCCApkCAQIxggEvooIBKwIBBDCB7gRUTAAAAAAAAAABAAAAS0RTSwYAAABqAQAAGwAAAAAAAAANmI+vcSayPiEeRxVf6EtDIAAAAIdIrMI9Rj3y1VPfv7dNFPQuBc9I/Ot0zPLHr9bBoVFZMIGVBgkrBgEEAYI3SgEwgYcGCisGAQQBgjdKAQ0weTB3MHUMBERTVFMMbXVzZWFzdC1ka2RzLmRrZHMuY29yZS53aW5kb3dzLm5ldDtodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1lO2N3YXBwcm94eWRrZHNuYW0wCwYJYIZIAWUDBAEtBCgFimJHgvag9mxSsOiUF4q3fOh+AfXBSS9Pj+I7iBnRnoI2FeWRZtvmMIIBXwYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwinYrTYyL6CMB/6YICARCAggEw+o1DKLNJDwxPQIqmN4XCUA36fcn+qYCI3P1LOXM0sv93aXI6Vu2kK3csNx/WyxZHRxi+Z9uKltZ0WSFBLEqNDsKn8MaFatrD5bFcUpE23aTOTffxp3XJDOjAKh26jp0qnFqjqN3HwWLFvz31+XRgJHmAdp2UsbYF6bnjmzUREt3Vq0VaM+/vHvmBNz6GRi7VDb9DL2NP0oQl7BIMWFA6ZfvGwMmMgNJOW/WfYPdsGaUPuYKjp9nOl2KU+Ohne5P3D0TmDC6Sj0n4pt1xI3oYEzQ1DDuQAwlKBd0C2t/iNuHhi6P2y+3sPj4bz6VRggxwlvB6ZxRh8yydZmIc8PmQZOSHDqlzdFZg1OCgLdU2gsQn1vVdJh0L6QzT6NRjpTvocHKvtbK0TtvD1uAW18BnvA==;"}
s = requests.Session()
s.cookies.update(cookies)

p = bs4.BeautifulSoup(requests.get("https://cams.floridapoly.edu/student/login.asp", cookies = cookies).text)

terms = {o.text.strip():o['value'] for o in p.select('option')}
assert len(terms) == len(p.select('option')) # no name collision

print([*reversed([o.text.strip() for o in p.select('option')])])

tid = terms[term]

print(f'txtUsername={u}&txtPassword={pw}&term={tid}&accessKey=&op=login')
r = s.post("https://cams.floridapoly.edu/student/ceProcess.asp", 
 headers = {"content-type": "application/x-www-form-urlencoded"},
 data = f'txtUsername={u}&txtPassword={pw}&term={tid}&accessKey=&op=login'
)

# scrape cams for course info

courses = []

p = bs4.BeautifulSoup(s.post("https://cams.floridapoly.edu/student/cePortalOffering.asp", 
 headers= {"content-type": "application/x-www-form-urlencoded"},
 data=f"f_TermCalendarID={tid}&page=1"
).text)

n = int(re.fullmatch(r'Viewing Page #1 \(Total Pages: (\d+)\)', p.select_one('.Portal_Grid_Pager').contents[-1].strip()).groups()[0])

for i in range(1, n + 1):
 p = bs4.BeautifulSoup(s.post("https://cams.floridapoly.edu/student/cePortalOffering.asp", 
  headers= {"content-type": "application/x-www-form-urlencoded"},
  data=f"f_TermCalendarID={tid}&page={i}"
 ).text)


 for a,b in zip(p.select('tr.courseInfo'),p.select('tr.courseInfo+*+*')):
  #print("AAA", a)
  #print("BBB", b)
  code = a.select('td')[0].contents[0].strip()
  name = a.select('td')[1].text.strip()
  print(code,name)
  if len(b.select('tr')) > 1:
   instr = b.select('tr')[1].select('td')[1].text.strip()
   room = b.select('tr')[1].select('td')[2].text.strip()
   days = b.select('tr')[1].select('td')[3].text.strip()
   start = b.select('tr')[1].select('td')[5].text.strip()
   end = b.select('tr')[1].select('td')[6].text.strip()
   print(instr,room,days,start,end)
  else:
   instr = None
   room = None
   days = None
   start = None
   end = None
  courses.append((code,name,instr,room,days,start,end))
  #break

import json

json.dump(courses, open('courses.json','w'))