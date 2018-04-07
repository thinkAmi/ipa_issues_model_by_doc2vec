import pathlib

from googleapiclient.http import MediaFileUpload

from google_drive_utils import (
    create_directory, get_directory_id, get_google_drive_service
)

# pdfをGoogle DocsにすることでOCRしてくれる
# MIME typeは以下にある
# https://developers.google.com/drive/v3/web/mime-types
MIME_TYPE = 'application/vnd.google-apps.document'

# Googleドライブ上のディレクトリ名
GOOGLE_DRIVE_DIRECTORY_NAME = 'ipa2'


def main():
    dir_id = get_directory_id(GOOGLE_DRIVE_DIRECTORY_NAME)
    if not dir_id:
        dir_id = create_directory(GOOGLE_DRIVE_DIRECTORY_NAME)

    upload_with_ocr(dir_id, 'ap')
    upload_with_ocr(dir_id, 'koudo')


def upload_with_ocr(directory_id, issue_type):
    service = get_google_drive_service()

    local_files = pathlib.Path(__file__).parent.glob(f'issues/{issue_type}/*.pdf')
    for f in local_files:
        media_body = MediaFileUpload(f, mimetype=MIME_TYPE, resumable=True)
        body = {
            # 拡張子付、パスなしのファイル名を与える
            # 拡張子なし(file_path.stem)だと、HTTP400エラーになる
            'name': f.name,
            'mimeType': MIME_TYPE,
            'parents': [directory_id],
        }

        r = service.files().create(
            body=body,
            media_body=media_body,
            # OCRの言語コードは、ISO 639-1 codeで指定
            # https://developers.google.com/drive/v3/web/manage-uploads
            ocrLanguage='ja',
        ).execute()
        print(f'upload result: {r}')


if __name__ == '__main__':
    main()

