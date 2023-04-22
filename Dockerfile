FROM python:3
ADD requirements.txt /
RUN pip install -r requirements.txt
ADD encryptedSECRET.txt /
ADD refKeySECRET.txt /
ADD encryptedACCESS.txt /
ADD refKeyACCESS.txt /
ADD main.py /
CMD [ "python", "./main.py" ]