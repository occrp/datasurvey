FROM python:2.7.9
MAINTAINER Smári McCarthy <smari@occrp.org>
    
RUN mkdir -p /usr/src/datasurvey
WORKDIR /usr/src/datasurvey

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/datasurvey/
RUN pip install -r requirements.txt

COPY . /usr/src/datasurvey/
RUN mkdir -p /var/log/datasurvey/

CMD ["/bin/bash"]
