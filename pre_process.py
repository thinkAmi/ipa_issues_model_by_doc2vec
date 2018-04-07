import pathlib
import re

OCR_AP = {
    'dir': 'ap',
    'last': '問80'
}
OCR_KOUDO = {
    'dir': 'koudo',
    'last': '問30',
}

# 最後の問題が終わったと判断するための正規表現
AFTER_LAST_QUESTION = re.compile(r'[0-9]|-')


def main():
    split_by_question(OCR_AP)
    split_by_question(OCR_KOUDO)


def split_by_question(ocr_type):
    # https://docs.python.jp/3/library/pathlib.html
    from_dir = pathlib.Path(__file__).resolve() \
        .parent.joinpath('ocr').joinpath(f'{ocr_type["dir"]}')

    to_dir = pathlib.Path(__file__).resolve() \
        .parent.joinpath('formatted_files').joinpath(f'{ocr_type["dir"]}')
    if not to_dir.exists():
        to_dir.mkdir(parents=True)

    local_files = pathlib.Path(from_dir).glob('*')
    for local_file in local_files:
        with open(local_file, 'r') as r:
            is_start = False
            is_start_msg = False
            is_last = False
            question_index = 1
            data = ''
            for row in r:
                if '問1から' in row:
                    is_start_msg = True

                # 問1の開始条件
                # ・"問1 "が出現した時
                # ・"「問1 "が出現した時
                # ・それまでに"問1から"という文言があり、"問1"という行が出現した時
                if row.startswith('問1 ') \
                        or row.startswith('「問1 ') \
                        or (is_start_msg and row.startswith('問1') and not row.startswith('問1から')):
                    is_start = True

                if not is_start:
                    continue

                # 問題が切り替わったので、ファイルを出力する時の条件
                # ・次の問題番号が出現した時
                # ・以下のようにOCRがうまくできなかった時
                #   ・現在が問32で、次が"問3 "で始まる時
                #   ・現在が問43で、次が"問4 "で始まる時
                #   ・現在が問70で、次が"71 "で始まる場合
                if row.startswith(f'問{question_index + 1}') \
                        or (question_index == 32 and row.startswith('問3 ')) \
                        or (question_index == 43 and row.startswith('問4 ')) \
                        or (question_index == 70 and row.startswith('71 ')):
                    write_file(to_dir, local_file.stem, data, question_index)
                    data = ''
                    question_index += 1

                if row.startswith(f'{ocr_type["last"]}'):
                    is_last = True

                # 最後の問題を出力する条件
                # ・当初指定した最後の問題番号が含まれる列以降
                # ・最後の問題が終わったと判断するための正規表現にマッチ
                # ・問題番号が1以降(1の場合、OCRがうまくいってなくて、問題自体をテキストに落とせてない)
                if is_last and AFTER_LAST_QUESTION.match(row) and question_index != 1:
                    # 最終問題の問題が終わったとみなして、出力
                    write_file(to_dir, local_file.stem, data, question_index)
                    break

                # 末尾の改行コードは不要なので削除しておく
                data += row.strip()

        # 出力した問題数を表示(OCR結果によっては途中で問題数が打ち切られてしまうため)
        # 何らかの原因で、OCRでは問題を解析できなかった時は、出力しない旨を表示する
        # TODO pdfを分割後、問題部分だけGoogle Driveにアップロードすれば解決するかもしれない
        remarks = '' if question_index > 1 else ', 出力しませんでした'
        print(f'file: {local_file.stem}, count: {question_index}{remarks}')


def write_file(to_dir, file_name, data, question_index):
    path = to_dir.joinpath(f'{file_name}_{question_index}.txt')
    fixed_data = format_data(data)

    with open(path, 'w') as w:
        w.write(fixed_data)


def format_data(data):
    # 末尾に _ が連続することがあるため、削除しておく
    fixed_data = data.strip('_')
    # 先頭の「問*」を削除
    fixed_data = re.sub('問[0-9]+', '', fixed_data)
    fixed_data = fixed_data.replace(' ', '')
    return fixed_data


if __name__ == '__main__':
    main()
