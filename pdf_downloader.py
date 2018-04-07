import pathlib
import subprocess


# https://qiita.com/gricoRodriguez/items/97375b5233176235aba4
# https://stackoverflow.com/questions/24346872/python-equivalent-of-a-given-wget-command
# https://stackoverflow.com/questions/4944295/skip-download-if-files-exist-in-wget


def main():
    parent_dir = pathlib.Path(__file__).resolve().parent.joinpath('issues')

    wget('201*_ap_am_qs.pdf', parent_dir.joinpath('ap'))
    wget('201*_koudo_am1_qs.pdf', parent_dir.joinpath('koudo'))


def wget(target_file_name, destination_dir):
    if not destination_dir.exists():
        destination_dir.mkdir(parents=True)

    command = [
        'wget',
        'https://www.jitec.ipa.go.jp/1_04hanni_sukiru/_index_mondai.html',
        '-r',                    # 再帰的にダウンロードする
        '-np',                   # 親ディレクトリを取得対象にしない
        '-nc',                   # ダウンロード済のはダウンロードしない
        '-l', '2',               # 再帰ダウンロードする深さ：2
        '-w', '1',               # ダウンロードごとのWait
        '-A', target_file_name,  # ダウンロードファイル名のフィルタ
        '-P', destination_dir,   # ダウンロードしたものを保存するディレクトリ
        '-nd',                   # ディレクトリ構造を保持しない
    ]

    try:
        subprocess.call(command)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
