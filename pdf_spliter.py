# $ pip install pypdf2
# http://note.mokuzine.net/python-pdf-split/
# https://docs.python.jp/3/library/pathlib.html
# https://qiita.com/amowwee/items/e63b3610ea750f7dba1b
# https://blanktar.jp/blog/2015/07/python-pathlib.html
import pathlib

from PyPDF2 import PdfFileWriter, PdfFileReader


def main():
    split('ap')
    split('koudo')


def split(issue_type):
    parent_dir = pathlib.Path(__file__).resolve().parent
    from_dir = parent_dir.joinpath('issues').joinpath(issue_type)
    to_dir = parent_dir.joinpath('split_issues').joinpath(issue_type)
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    # 変換元ディレクトリに存在するファイル一覧を取得
    issues = list(from_dir.glob('*'))
    for issue in issues:
        with issue.open('rb') as r:
            source = PdfFileReader(r, strict=False)
            total_pages = source.getNumPages()

            for i in range(0, total_pages):
                output = PdfFileWriter()
                output.addPage(source.getPage(i))

                export_path = to_dir.joinpath(f'{issue.stem}_{i + 1}.pdf')
                with export_path.open('wb') as w:
                    output.write(w)


if __name__ == '__main__':
    main()
