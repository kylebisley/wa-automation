# find appropiate new applicants night
    #pull list of New Applicant Nights
    #if event was held this month
    #pull attendance list
# get list of those in attendance
# get list of level: map them to applying to fields
# for each attendie 
    # set to requested level
    # set pending new
    # generate invoice
    # email invoice
import json
from pprint import pprint
from datetime import datetime
from config import config
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from electronic_mail import electronic_mail
from email_recipient import email_recipient
import pdb
# To be run once a month at the end of the month. Generates an application for each member who attended 
# this months Applicants Night. 
def applying_for(contact):
    '''Returns the level id for level coresponding to the "Applying for" field if field not found or is type None returns the id for Regular Membership'''
    for i in contact['FieldValues']:
        if (i['FieldName'] == 'What are you applying for?'):
            print('************************************************************')
            level_map = {'Regular membership': '1113399',
                        'Reduced rate as a student': '1113401',
                        'Reduced rate for financial reasons': '1113401',
                        'Schneider Corporate Membership':'1113400',
                        'Annual membership': '1113394'}
            # if Empty then level id is 1113395 (cancel my membership)
            # pdb.set_trace()
            print(contact['Id'])
            if i['Value'] is None:
                return '1113399'
            else:
                return level_map.get(i['Value']['Label'], '1113395')
    return '1113399'

def auto_applications(session, contacts, now):
    temp = f'events?'
    events = session.request('GET', temp)
    #pprint(events)
    for event in events['Events']:
        event_date = datetime.strptime(event['EndDate'],'%Y-%m-%dT%H:%M:%S%z')
        #feb test
        soon = datetime.strptime('2020-03-3T20:30:00-08:00','%Y-%m-%dT%H:%M:%S%z')

        if ((event['Name'] == 'Applicants Evening')  & 
                 (event_date.month == now.month)):
            
            temp =f'eventregistrations/?eventId={event["Id"]}'
            event_reg = session.request('GET', temp)

            applications = []
            for registration in event_reg:
                if registration['IsCheckedIn']:
                    applications.append(contacts.list[registration['Contact']['Id']])
            for application in applications:
                temp =f'contacts/{application.ID}'
                contact = session.request('GET', temp)

                new_level = applying_for(contact)

                edit_dic ={
                            "Id": contact["Id"],
                            "MembershipEnabled" : "True",
                            "MembershipLevel" : {"Id" : new_level},
                            "Status" : "PendingNew"
                            }
                temp = f'contacts/{contact["Id"]}'
                response = session.request('PUT', temp, data=edit_dic)
                
                #send email 
                with open('./emails/application_approved.txt', 'r') as draft:
                    email_body = draft.read()
                contact = contacts.get_by_id(contact['Id'])
                email_body.format(contact.name)

                recipient = email_recipient(contact.ID, contact, 0)

                # constructs electronic_mail object and converts object to json
                mail = electronic_mail('Makerspace Application Approved', email_body, [recipient])
                j_mail = json.dumps(mail, default=electronic_mail.convert_to_dic)

                # API call to send email
                contacts.session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))

    print('onewards and upwards')
