import argparse
import pathlib
import pprint

from gensim.models.doc2vec import Doc2Vec

from doc2vec_runner import morphological_analysis

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-y', '--year', action='store', required=True, type=int,
                    help='試験年(西暦)')
parser.add_argument('-t', '--term', action='store', required=True, choices=['a', 'h'],
                    help='試験時期(a:秋, h:春)')
parser.add_argument('-q', '--question', action='store', type=int,
                    help='問題番号')
parser.add_argument('-s', '--similarity', action='store_true', default=False,
                    help='一番の類似問題番号を表示する')
parser.add_argument('-n', '--ntop', action='store', type=int,
                    help='上位n件の類似を表示する')


MODEL_NAME = 'ipa_issues_30.model'


def similarity(year, term):
    model = get_model()

    for i in range(1, 31):
        top_index = 0
        top_value = 0
        for j in range(1, 81):
            current_value = model.docvecs.similarity(
                f'{year}h{to_heisei(year)}{term}_koudo_am1_qs_{i}',
                f'{year}h{to_heisei(year)}{term}_ap_am_qs_{j}'
            )
            if top_value < current_value:
                top_value = current_value
                top_index = j

        print(f'高度: {i}, 応用: {top_index}, 類似度: {top_value}')


def most_similar(year, term, question, ntop):
    model = get_model()

    file_name = f'{year}h{to_heisei(year)}{term}_koudo_am1_qs_{question}.txt'

    full_path = pathlib.Path(__file__).resolve() \
        .parent.joinpath('formatted_files').joinpath('koudo').joinpath(file_name)

    with open(full_path, 'r') as f:
        doc = f.read()
        words = morphological_analysis(doc)

        # ベクトル化して類似しているものを探す
        vec = model.infer_vector(words)
        result = model.docvecs.most_similar([vec], topn=ntop)

        season = '春' if term == 'a' else '秋'
        print(f'高度試験({year}年{season})と類似した問題')
        pprint.pprint(result)


def get_model():
    model_file = pathlib.Path(__file__).resolve().parent \
        .joinpath('model').joinpath(MODEL_NAME)
    return Doc2Vec.load(str(model_file))


def to_heisei(year):
    return year - 1988


if __name__ == '__main__':
    args = parser.parse_args()

    if args.similarity:
        most_similar(args.year, args.term, args.question, args.ntop)
    else:
        similarity(args.year, args.term)
