'''To be run on the first of the month. For every attendant of New Applicant Night
of the previous month the following actions are performed. 1)level is set to
Applying for field choice. 2)Invoice is changed to include only Membership dues and
Access card. 3)application_approved email is sent to inform them of the invoice'''
import json
from datetime import datetime
# from config import config
# from datetime import timedelta
from dateutil.relativedelta import relativedelta
from electronic_mail import electronic_mail
from email_recipient import email_recipient

def applying_for(contact):
    '''Returns the level id "Applying for" field. If field not found
    or is type None return id for Regular Membership'''

    for field in contact['FieldValues']:
        if field['FieldName'] == 'What are you applying for?':
            level_map = {'Regular membership': '1113399',
                         'Reduced rate as a student': '1113401',
                         'Reduced rate for financial reasons': '1113401',
                         'Schneider Corporate Membership':'1113400',
                         'Annual membership': '1113394'}
            if field['Value'] is None:
                return '1113399'
            else:
                return level_map.get(field['Value']['Label'])
    return 'Already set'

def get_applications(event_reg, contacts):
    '''Returns list of Id's of contacts who's applications should be processed'''
    applications = []
    for registration in event_reg:
        if registration['IsCheckedIn']:
            applications.append(contacts.list[registration['Contact']['Id']])
    return applications

def set_membership(session, contact):
    '''Changes membership to level returned by applying_for'''
    new_level = applying_for(contact)
    if new_level == 'Already set':
        return False

    edit_dic = {"Id": contact["Id"],
                "MembershipEnabled" : "True",
                "MembershipLevel" : {"Id" : new_level},
                "Status" : "PendingNew"}
    temp = f'contacts/{contact["Id"]}'
    session.request('PUT', temp, data=edit_dic)
    return True

def edit_invoice(session, contact_id):
    '''Sets invoice to have only membership cost and Card cost.'''
    temp = f'invoices?contactId={contact_id}'
    invoices = session.request('GET', temp)

    for invoice in invoices['Invoices']:
        if invoice['OrderType'] == 'MembershipApplication':

            temp = f'invoices/{invoice["Id"]}'
            invoice = session.request('GET', temp)

            order_details = invoice['OrderDetails']
            invoice_update = {'Notes': 'Access Card: Fee to VITP park security for new card.',
                              'Taxes': None,
                              'Value': 11.20}
            for line_item in order_details:
                if line_item['OrderDetailType'] == 'MemberLevel':
                    invoice_data = {'DocumentNumber': invoice['DocumentNumber'],
                                    'Id': invoice['Id'],
                                    'OrderDetails':[line_item, invoice_update]}

            temp = f'invoices/{invoice["Id"]}'
            session.request('PUT', temp, data=invoice_data)

def send_invoice_mail(session, contact):
    '''Sends email to new member informing them of outstanding invoice'''
    with open('./emails/application_approved.txt', 'r') as draft:
        email_body = draft.read()
    email_body.format(contact.name)
    recipient = email_recipient(contact.ID, contact, 0)

    # constructs electronic_mail object and converts object to json
    mail = electronic_mail('Makerspace Application Approved', email_body, [recipient])
    j_mail = json.dumps(mail, default=electronic_mail.convert_to_dic)
    # API call to send email
    session.request('POST', 'email/SendEmail', rpc=True, data=json.loads(j_mail))

def auto_applications(session, contacts, now):
    ''' To be run once a month on the first day of the month.
    Generates an application for each member who attended this
    months Applicants Night. '''
    temp = f'events?'
    events = session.request('GET', temp)

    for event in events['Events']:
        event_date = datetime.strptime(event['EndDate'], '%Y-%m-%dT%H:%M:%S%z')
        last_month = now + relativedelta(months=-1)
        if ((event['Name'] == 'Applicants Evening')
                & (event_date.month == last_month.month)):

            temp = f'eventregistrations/?eventId={event["Id"]}'
            event_reg = session.request('GET', temp)

            applications = get_applications(event_reg, contacts)

            for application in applications:
                temp = f'contacts/{application.ID}'
                contact = session.request('GET', temp)
                change = set_membership(session, contact)
                # when false email and invoice edit is unnecessary
                if change:
                    edit_invoice(session, contact['Id']) #add door card to invoice
                    #send email
                    contact = contacts.get_by_id(contact['Id'])
                    send_invoice_mail(session, contact)
