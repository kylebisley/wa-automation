# find appropiate new applicants night
    #pull list of New Applicant Nights
    #if event was held this month
    #pull attendance list
# get list of those in attendance
# for each attendie 
    # set to requested level
    # set pending new
    # generate invoice
    # email invoice
from pprint import pprint
from datetime import datetime
from config import config
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pdb

def auto_applications(session, contacts, now):
    temp = f'events?'
    events = session.request('GET', temp)
    #pprint(events)
    for event in events['Events']:
        event_date = datetime.strptime(event['EndDate'],'%Y-%m-%dT%H:%M:%S%z')
        if ((event['Name'] == 'Applicants Evening')  & 
                (event_date > (now - relativedelta(months=1)))):
            print('now-timedelta')
            print(now - relativedelta(months=1))

            print(event['EndDate'])
            # 
            # print("event_date")
            # print(type(event_date))
            # print(event_date)
            # print('*****')

            # event_date = event_date - timedelta(30)
            # print("event_date - timedelta(30)")
            # print(event_date)
            # print()
            # print()
            # temp = f'events/{event["Id"]}'
            # event_details = session.request('GET', temp)
            # print('************************************************************')
            # #pprint(event_details)
            
            # temp =f'eventregistrations/?eventId={event["Id"]}'
            # event_reg = session.request('GET', temp)
            # print('************************************************************')
            # print('************************************************************')
            # #pprint(event_reg) 
            # applications = []
            # print("RSVP'ed")
            # for registration in event_reg:
            #     print(registration['Contact']['Name'])
            #     if registration['IsCheckedIn']:
            #         #print(registration['Contact']['Name'])
            #         applications.append(registration['Contact']['Id'])
            # print('Is Checked IN!!!!!!!')
            # for i in applications:
            #     print(i)
            
            
    

    print('onewards and upwards')
#events[event][0]['Name']
