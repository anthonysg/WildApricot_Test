__author__ = 'dsmirnov@wildapricot.com'

import WaApi
import urllib.parse
import json
from datetime import datetime

def get_10_active_members():
    params = {'$filter': 'member eq true',
              '$top': '10',
              '$async': 'false'}
    request_url = contactsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Contacts


def last_day_of_month(any_date_in_specific_month):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)

eventsUrl = next(res for res in account.Resources if res.Name == 'Events').Url

def get_current_month_events(): #Fetches Events for the current month.
    firstDayOfCurrentMonth = datetime.today().replace(day=1) #Get first day of month
    lastDayOfCurrentMonth = ast_day_of_month(datetime.today()) #Get last day of month
    firstDayOfCurrentMonth_String = firstDayOfCurrentMonth.strftime('%Y-%m-%d') #In YYYY-MM-DD format.
    lastDayOfCurrentMonth_String = lastDayOfCurrentMonth.strftime('%Y-%m-%d')

    #f-strings in Python >= 3.6, denoted with an f at the beginning of a string.
    params = {'$filter': f'StartDate gt {firstDayOfCurrentMonth_String} AND StartDate lt {lastDayOfCurrentMonth_String}', #Originally was $filter': 'StartDate gt 2019-01-01 AND StartDate lt 2015-01-31'
              '$async': 'false'}
    request_url = eventsUrl + '?' + urllib.parse.urlencode(params)
    print(request_url)
    return api.execute_request(request_url).Events

#Potential Improvements:
    #-Dynamically generate date object to correspond to the chosen month for the calendar, then use that to generate string in correct format.
    #-Use Paging to not have to perform query for each month by fetching an entire year's worth of events (or more) at once?
    #-Potentially sort them?


def print_contact_info(contact):
    print('Contact details for ' + contact.DisplayName + ', ' + contact.Email)
    print('Main info:')
    print('\tID:' + str(contact.Id))
    print('\tFirst name:' + contact.FirstName)
    print('\tLast name:' + contact.LastName)
    print('\tEmail:' + contact.Email)
    print('\tAll contact fields:')
    for field in contact.FieldValues:
        if field.Value is not None:
            print('\t\t' + field.FieldName + ':' + repr(field.Value))


def create_contact(email, name):
    data = {
        'Email': email,
        'FirstName': name}
    return api.execute_request(contactsUrl, api_request_object=data, method='POST')


def archive_contact(contact_id):
    data = {
        'Id': contact_id,
        'FieldValues': [
            {
                'FieldName': 'Archived',
                'Value': 'true'}]
    }
    return api.execute_request(contactsUrl + str(contact_id), api_request_object=data, method='PUT')

# How to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication
api = WaApi.WaApiClient("CLIENT_ID", "CLIENT_SECRET")
api.authenticate_with_contact_credentials("ADMINISTRATOR_USERNAME", "ADMINISTRATOR_PASSWORD")
accounts = api.execute_request("/v2/accounts")
account = accounts[0]

print(account.PrimaryDomainName)

contactsUrl = next(res for res in account.Resources if res.Name == 'Contacts').Url

# get top 10 active members and print their details
#contacts = get_10_active_members()
#for contact in contacts:
    #print_contact_info(contact)

# create new contact
#new_copntact = create_contact('some_email1@invaliddomain.org', 'John Doe')
#print_contact_info(new_copntact)

# finally archive it
#archived_contact = archive_contact(new_copntact.Id)
#print_contact_info(archived_contact)

# get Events and print their details
events = get_current_month_events()
for event in events:
    print('\tID:' + str(event.Id))
    print('\tEventType:' + event.EventType)
    print('\tName:' + event.Name)
    if (event.StartTimeSpecified == true)
        print('\tStart Date:' + event.StartDate)
    else
        print('\tNo Start Date Specified.')
