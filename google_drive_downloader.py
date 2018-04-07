import pathlib

from googleapiclient.http import MediaIoBaseDownload

from google_drive_utils import get_google_drive_service, list_files

# Googleドライブ上のディレクトリ名
GOOGLE_DRIVE_DIRECTORY_NAME = 'ipa2'


def main():
    service = get_google_drive_service()
    download(service, 'ap')
    download(service, 'koudo')


def download(service, issue_type):
    # https://docs.python.jp/3/library/pathlib.html
    directory = pathlib.Path(__file__).resolve().parent.joinpath('ocr').joinpath(f'{issue_type}')
    if not directory.exists():
        directory.mkdir(parents=True)

    drive_files = list_files(GOOGLE_DRIVE_DIRECTORY_NAME, service)
    for drive_file in drive_files['files']:
        file_name = pathlib.Path(f'{drive_file["name"]}').stem + '.txt'
        if issue_type not in file_name:
            continue
        full_path = directory.joinpath(file_name)
        print(full_path)

        # https://developers.google.com/drive/v3/web/manage-downloads
        request = service.files().export_media(fileId=drive_file['id'],
                                               mimeType='text/plain')
        with open(full_path, mode='wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                _, done = downloader.next_chunk()


if __name__ == '__main__':
    main()
