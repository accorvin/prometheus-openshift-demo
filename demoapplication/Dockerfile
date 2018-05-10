FROM fedora

RUN mkdir /demoapplication
WORKDIR /demoapplication
COPY . /demoapplication

RUN pip-3 install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ./demoapplication.py
