FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -y python
RUN apt-get install -y python-pip
RUN apt-get clean all
RUN pip install protobuf==2.6.1
RUN pip install pika==0.9.8

ADD . /platform-python
WORKDIR /platform-python
# RUN pip install -r /platform-python/requirements.txt

CMD python -m microplatform.tests