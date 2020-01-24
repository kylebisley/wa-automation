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
import pdb

def auto_applications(session, contacts, now):
    temp = f'events?'
    events = session.request('GET', temp)
    #pprint(events)
    for event in events['Events']:
        if (event['Name'] == 'Applicants Evening'):
            print('************************************************************')           
            #pprint(event)
            print(event['Name'])
            temp = f'events/{event["Id"]}'
            event_details = session.request('GET', temp)
            print('************************************************************')
            #pprint(event_details)
            
            temp =f'eventregistrations/?eventId={event["Id"]}'
            event_reg = session.request('GET', temp)
            print('************************************************************')
            print('************************************************************')
            pprint(event_reg)
            applications = []
            for registration in event_reg:
                if registration['IsCheckedIn']:
                    print(registration['Contact']['Name'])
                    applications.append(registration['Contact']['Id'])
                    print('Is Checked IN!!!!!!!')
    

    print('onewards and upwards')
#events[event][0]['Name']
