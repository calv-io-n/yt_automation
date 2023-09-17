#!/usr/bin/python3
import os.path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Load the service account credentials
SERVICE_ACCOUNT_FILE = './util/input/token.json'
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def upload_to_drive(filename, mimetype='video/mp4', folder_id='1unhTeJ1gvCn7Uc-ZUKhLHPcXuj1NnlHY'):
    # Build the Drive v3 API client
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {'name': os.path.basename(filename)}
    if folder_id:  # if a folder ID is provided, set it as the parent folder
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(filename, mimetype=mimetype)
    try:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'File ID: {file.get("id")}')
    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    filename = '/usr/src/app/sub_output.mp4'
    upload_to_drive(filename)
