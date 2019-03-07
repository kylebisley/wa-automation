from config import config
from datetime import datetime, timezone

def accessflag(contacts, now):
    """
    Cancels security access cards for members who have volentarily cesed paying.
    """

    access_to_cancel = ' '
    for contact in contacts.getlevel(*config['accessflag']['levels']:
        if contact.accessflag != 'True' : contact.accessflag = 'True'
            continue
    for contact in contacts:
        if contact.level in *config['accessflag']['levels']:
            contact.accessflag = 'True'
            continue
        elif accessflag == 'True': 
            access_to_cancel = ', '.join([f'"{contact.email}"')
            contact.accessflag == 'False'
            continue

    #pass "email function" list of people to include in an email to security
