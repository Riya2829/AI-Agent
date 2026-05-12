from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
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