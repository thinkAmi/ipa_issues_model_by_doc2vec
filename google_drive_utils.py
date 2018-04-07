import argparse
import os

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# pdfをGoogle DocsにすることでOCRしてくれる
# MIME typeは以下にある
# https://developers.google.com/drive/v3/web/mime-types
MIME_TYPE = 'application/vnd.google-apps.document'

# get_credentials()関数まわりは公式ドキュメントよりコピペ(Python2.6部分は削除)
# https://developers.google.com/drive/v3/web/quickstart/python#step_3_set_up_the_sample

# scopeは以下より
# https://developers.google.com/drive/v3/web/about-auth
SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'ipa-google-drive-api-client'

flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()


def get_google_drive_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('drive', 'v3', http=http)


def create_directory(directory_name, service=None):
    s = service if service else get_google_drive_service()

    body = {
        'name': directory_name,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    result = s.files().create(body=body).execute()
    return result['id']


def list_files(directory_name, service=None):
    s = service if service else get_google_drive_service()
    dir_id = get_directory_id(directory_name, s)

    result = s.files().list(
        # https://developers.google.com/drive/v3/web/search-parameters
        q=f'"{dir_id}" in parents',
        # https://developers.google.com/drive/v3/web/search-parameters
        fields='files(id, name)'
    ).execute()
    return result

    # 取得結果
    # {'files': [
    #  {'id': 'xxx', 'name': '2017h29h_ap_am_qs.pdf'},
    #  {'id': 'xxx', 'name': '2017h29a_ap_am_qs.pdf'},
    #  ...
    # ]}


def get_directory_id(directory_name, service=None):
    s = service if service else get_google_drive_service()
    result = s.files().list(q=f'name="{directory_name}"').execute()
    if not result['files']:
        return ''
    return result['files'][0]['id']


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials
