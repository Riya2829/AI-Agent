import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

google_creds = os.getenv("GOOGLE_CREDENTIALS_JSON")

credentials_info = json.loads(google_creds)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=SCOPES
)

service = build('drive', 'v3', credentials=credentials)

def search_drive(query):

    results = service.files().list(
        q=query,
        pageSize=10,
        fields="files(id, name, mimeType, modifiedTime, webViewLink)"
    ).execute()

    return results.get('files', [])
