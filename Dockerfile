FROM python:2.7.9
MAINTAINER Smári McCarthy <smari@occrp.org>
    
RUN mkdir -p /datasurvey
WORKDIR /datasurvey

RUN pip install --upgrade pip
COPY requirements.txt /datasurvey/
RUN pip install -r requirements.txt

COPY . /datasurvey/
RUN mkdir -p /var/log/datasurvey/

CMD ["/bin/bash"]
