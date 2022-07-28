# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 00:03:09 2021

@author: Jaskaran S. Purewal
"""

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class Drive():
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/drive']#deleting readonly will give me full access to the drive
        #as permissions are changed it will ask to authenticate once
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        #everytime a new mydrive is initialised , login automatically
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret_466342191281-69fcje5jtt14dvbgtv2pkltgr47pj4ld.apps.googleusercontent.com.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
    
        self.service = build('drive', 'v3', credentials=creds)

    def list_contents(self,pagesize=5):
        results = self.service.files().list(
        pageSize=pagesize, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
    
        if not items:
            print('No files found.')
        else:
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
def main():
    test1=Drive()
    test1.list_contents()        

if __name__ == '__main__':
    main()