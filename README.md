# ipa_issues_model_by_doc2vec

Create IPA issues model and Show similarity question by gensim Doc2Vec.

　  
## Tested Environment

- Mac OS X 10.11.6
- Python 3.6.5
- JUMAN++
- Gensim 3.4.0
- google-api-python-client 1.6.6
- pyknp 0.3
- (PyPDF2 1.26.0)

　  
## Install
### Python packages

```
$ pip install -r requirements.txt 
```

　  
### JUMAN++

for Mac.

```
$ brew install jumanpp
```

　  
## Usage
### Create Google Drive API project

https://developers.google.com/drive/v3/web/quickstart/python

　  
### Create training models

```
# issue pdf download
$ python pdf_downloader.py 

# upload Google Drive with OCR
$ python google_drive_uploader.py

# download Google Drive
$ python google_drive_downloader.py

# pre-process
$ python pre_process.py

# create Doc2Vec model and training
$ python doc2vec_runner.py
```

　  
### Show result

```
# most simirality
# e.g. 2017年春の高度試験の午前1と一番類似している応用情報技術者試験の問題番号
$ python similarity_runner.py -y 2017 -t h

# top n simirality
# e.g. 2017年春の高度試験の問1と類似している上位10件
$ python similarity_runner.py -y 2017 -t h -q 1 -s -n 10
```

　  
## License

MIT
