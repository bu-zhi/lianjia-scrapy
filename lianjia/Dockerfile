FROM python:3.8-slim
ENV PATH /usr/local/bin:$PATH
ADD . /data
WORKDIR /data
RUN pip3 install -r requirements.txt
CMD scrapy crawl lj
