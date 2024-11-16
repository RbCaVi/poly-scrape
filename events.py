import requests
import json
import datetime

y,m,d = 2024,11,12

def fetch(url, options):
 if options.get('method') == 'POST':
  f = requests.post
 else:
  f = requests.get
 return f(url, headers = options.get('headers', {}), data = options.get('body'))

def adel(d, k, v):
 assert d[k] == v, f'd[{k}]: {d[k]} != {v}'
 del d[k]

def adeld(d, dk):
 for k,v in dk.items():
  adel(d, k, v)

def aset(d, k, v):
 assert d.get(k, v) == v
 d[k] = v

events = {}

count = 0

for start in range(24):
 r = requests.post("https://events.floridapoly.edu/EmsWebApp/ServerApi.aspx/BrowseEvents",
  headers = {"content-type": "application/json"},
  data = json.dumps({
   'filterData': {
    'filters': [
     {'filterName': 'StartDate', 'value': f'{y:04}-{m:02}-{d:02} {start}:00:00', 'filterType': 3},
     {'filterName': 'TimeZone', 'value': '61', 'displayValue': '', 'filterType': 2},
    ]
   }
  })
 )

 data = json.loads(r.json()['d'])

 adel(data, 'MonthlyBookingResults', [])
 adel(data, 'Holidays', [])
 adel(data, 'ListDate', "0001-01-01T00:00:00")
 adel(data, 'ShowLocation', False)
 adel(data, 'ShowEndTime', False)
 adel(data, 'ShowGroupName', False)
 adel(data, 'UserCanViewLocations', False)
 adel(data, 'RollupBookingsToReservation', False)
 adel(data, 'BrowseEventsDefaultDisplayFormat', 0)
 adel(data, 'BrowseNumberOfEventsToDisplayOnDailyView', 50)
 adel(data, 'BrowseNumberOfEventsToDisplayOnWeeklyView', 200)
 adel(data, 'BrowseNumberOfEventsToDisplayOnMonthlyView', 200)
 adel(data, 'BrowseEventsShowGroupTypeDropDown', False)
 adel(data, 'BrowseEventsShowRoomTypeDropDown', False)
 adel(data, "Filters", {
  'Filters': [],
  'RequiredFilters': [
   {'filterLabel': 'Date', 'hide': False, 'required': True, 'linkedFilterName': 'EndDate', 'linkedFilterType': 3, 'linkedFilterInterval': 1, 'defaultDisplayValue': None, 'filterName': 'StartDate', 'value': f'{datetime.datetime.today().strftime("%Y-%m-%d")} 12:00:00', 'displayValue': None, 'filterType': 3},
   {'filterLabel': 'Date', 'hide': True, 'required': True, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'EndDate', 'value': f'{(datetime.datetime.today() +  datetime.timedelta(days = 1)).strftime("%Y-%m-%d")} 12:00:00', 'displayValue': None, 'filterType': 3},
   {'filterLabel': 'Time Zone', 'hide': True, 'required': True, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'TimeZone', 'value': '61', 'displayValue': None, 'filterType': 2}
  ],
  'OptionalFilters': [
   {'filterLabel': 'Locations', 'hide': False, 'required': False, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'Locations', 'value': '-1', 'displayValue': 'All', 'filterType': 8},
   {'filterLabel': 'Room', 'hide': False, 'required': False, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'Room', 'value': '', 'displayValue': '', 'filterType': 1},
   {'filterLabel': 'Department/Event Host Name', 'hide': False, 'required': False, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'GroupName', 'value': '', 'displayValue': '', 'filterType': 1},
   {'filterLabel': 'Event Name', 'hide': False, 'required': False, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'EventName', 'value': '', 'displayValue': '', 'filterType': 1},
   {'filterLabel': 'Event Type', 'hide': False, 'required': False, 'linkedFilterName': None, 'linkedFilterType': None, 'linkedFilterInterval': None, 'defaultDisplayValue': None, 'filterName': 'EventTypes', 'value': '', 'displayValue': '', 'filterType': 7}
  ]
 })
 #print(data['NextBookingDate']) # not important
 #print(data['DailyCounts']) # processed below
 c = data['DailyCounts'].get(f'{m}/{d}/{y}', 0)
 count = max(count, c)

 for x in data['DailyBookingResults']:
  adeld(x, {
   'InternalId': 0,
   'EventCount': 0,
   'GroupId': 0,
   'FloorID': 0,
   'Floor': None,
   'ImageHeight': 0,
   'ImageWidth': 0,
   'RoomOverrideDescription': None,
   'ShowFloorMap': False,
   'Setup': None,
   'VideoConferenceHost': False,
   'ChangeHost': False,
   'EventTime': None,
   'ReserveType': 0,
   'StatusType': 0,
   'Status': None,
   'ImageId': 0,
   'IsCheckedIn': False,
   'CanCheckIn': False,
   'RequiresCheckIn': False,
   'CheckInMinutes': 0,
   'AllowCancel': False,
   'AllowCancelPamInstance': False,
   'RequiresCancelReason': False,
   'DefaultCancelReason': 0,
   'AllowEndNow': False,
   'AllowEdit': False,
   'EditBtnAltText': None,
   'EditBtnFunctionType': None,
   'EditBtnFunctionValue': None,
   'ShowAddServices': False,
   'HasServices': False,
   'AddServicesFunctionValue': None,
   'EventLink': None,
   'TotalNumberOfBookings': 0,
   'WebUserIsOwner': False,
   'IsHoliday': False,
   #'IsAllDayEvent': False,
   'TimezoneAbbreviation': 'ET',
   'OccurrenceCount': 0,
   'IsCalendaringEnabled': False,
   'IsSkypeEnabled': False,
   'IsTeamsEnabled': False,
   'IsWebexEnabled': False,
   'IsZoomEnabled': False,
   'UserEventStart': '0001-01-01T00:00:00',
   'UserEventEnd': '0001-01-01T00:00:00',
   'EventGmtStart': '0001-01-01T00:00:00',
   'EventGmtEnd': '0001-01-01T00:00:00',
   'ConferenceURL': None,
   'ConferencingSolution': None,
   'Date': None,
   'ShowCheckinButton': False,
  })
  # not important - ['EventStart'] is better (and is the one shown on the website)
  del x['GmtStart']
  del x['GmtEnd']
  del x['TimeBookingStart']
  del x['TimeBookingEnd']
  # probably not important
  del x['LocationLink']
  del x['ReservationSummaryUrl']
  del x['ReservationId']
  if x['EventStart'].startswith(f'{y:04}-{m:02}-{d:02}T'):
   if not x['EventEnd'].startswith(f'{y:04}-{m:02}-{d:02}T'):
    #print(x)
    pass
   aset(events, x['Id'], x)

import re
def extracttime(t):
 mat = re.match(f'{y:04}-{m:02}-{d:02}T'r'(\d\d):(\d\d):00', t)
 if mat is not None:
  time = mat.groups()
  return time[0] + time[1]
 else:
  mat = re.match(f'{y:04}-{m:02}-{d + 1:02}T'r'00:00:00', t)
  if mat is not None:
   return '2400'
  else:
   print(t, 'has no time')
   return None

eventdata = []
for e in events.values():
 eventdata.append({
  'name': e['EventName'],
  'owner': e['GroupName'], # (who scheduled the event)
  'location': e['Location'],
  'building': e['Building'],
  #'BuildingId': e['BuildingId'],
  'room': e['Room'],
  #'RoomTypeId': e['RoomTypeId'],
  'roomtype': e['RoomType'],
  #'RoomCode': e['RoomCode'],
  #'StatusId': e['StatusId'],
  #'StatusTypeId': e['StatusTypeId'],
  #'IsAllDayEvent': e['IsAllDayEvent'],
  #'RoomId': e['RoomId'],
  'start': extracttime(e['EventStart']),
  'end': extracttime(e['EventEnd']),
  'id': len(eventdata)
 })

events = {
 'day': (y, m, d),
 'events': eventdata,
}

import json
with open('events.json', 'w') as f:
 json.dump(events, f)