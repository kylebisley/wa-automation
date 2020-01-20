from config import config
from contacts import Contacts
import contact
from pprint import pprint
import pdb
from datetime import datetime

    
def timeout(session, contacts, now):
    
    balance_due = contacts.balance_due()
    print('balance_due')
    pprint(balance_due)

    #fred blogs
    print('fred blogs')
    contact_id = str(53438595)
    temp = f'invoices?contactId={contact_id}'
    pprint(temp)
    invoices = session.request('GET', temp)
    # pprint(invoices)
    # print('DocumentDate')
    #pdb.set_trace()
    # print(type(invoices['Invoices'][0]['DocumentDate']))
    #ValueError: time data '2019-12-01T13:36:53+00:00' does not match format '%Y %b %d %H:%M:%S:%z''
    datetime_object = datetime.strptime(invoices['Invoices'][0]['DocumentDate'], '%Y-%m-%dT%H:%M:%S%z')
    
    
    # print('datetime')
    # print(type(datetime_object))
    # print(datetime_object)
    # print('now-datetime_object')
    # print(now-datetime_object)
    if (now - config['archive']['threshold'] <= datetime_object):
        print('')
        #send email
        #set level to new applicant
        #set contact to archived 
    print('')
    #kyle bisleys
    # print('kyle bisley')
    # contact_id = str(53359541)
    # temp = f'invoices?contactId={contact_id}'
    # pprint(temp)
    # invoices = session.request('GET', temp)
    # pprint(invoices)

