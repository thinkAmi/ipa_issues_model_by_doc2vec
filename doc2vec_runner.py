import pathlib

from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from pyknp import Jumanpp

# $ pip install http://lotus.kuee.kyoto-u.ac.jp/nl-resource/pyknp/pyknp-0.3.tar.gz
# http://tdoc.info/blog/2014/01/15/pip.html

LEARN_AP = 'ap'
LEARN_KOUDO = 'koudo'
EPOCHS = 30


def main():
    ap_trainings = get_trainings(LEARN_AP)
    koudo_trainings = get_trainings(LEARN_KOUDO)
    all_trainings = ap_trainings + koudo_trainings

    export_dir = pathlib.Path(__file__).resolve().parent.joinpath('model')
    if not export_dir.exists():
        export_dir.mkdir(parents=True)
    model_path = export_dir.joinpath(f'ipa_issues_{EPOCHS}.model')

    # トレーニング兼モデルの作成
    # https://radimrehurek.com/gensim/models/doc2vec.html#gensim.models.doc2vec.Doc2Vec
    # epochsをいれないと、まともな結果が出ない：過学習は気にしない
    # https://stackoverflow.com/questions/46807010/what-are-doc2vec-training-iterations
    # 引数iterがepochsへと変更になる
    # python3.6/site-packages/gensim/models/doc2vec.py:362: UserWarning: The parameter `iter` is deprecated, will be removed in 4.0.0, use `epochs` instead.
    # warnings.warn("The parameter `iter` is deprecated, will be removed in 4.0.0, use `epochs` instead.")
    model = Doc2Vec(
        documents=all_trainings,
        dm=1,                   # PV-DMモデルを使う
        min_count=1,            # これ以下の出現数の単語は無視
        workers=4,              # スレッドのワーカー数
        epochs=EPOCHS,          # エポック数
    )
    # PosixPathは受け付けてもらえないため、文字列にする
    model.save(str(model_path))


def get_trainings(issue_type):
    trainings = []
    paths = get_file_paths(issue_type)
    for p in paths:
        doc = read_file(p)
        words = morphological_analysis(doc)
        trainings.append(TaggedDocument(words=words, tags=[p.stem]))
        print(f'file read: {p}')
    return trainings


def get_file_paths(parent_dir):
    from_dir = pathlib.Path(__file__).resolve() \
        .parent.joinpath('formatted_files').joinpath(f'{parent_dir}')
    return pathlib.Path(from_dir).glob('*')


def read_file(path):
    with open(path, 'r') as f:
        return f.read()


def morphological_analysis(doc):
    r = Jumanpp().analysis(doc)
    return [mrph.midasi for mrph in r.mrph_list()]


if __name__ == '__main__':
    main()
