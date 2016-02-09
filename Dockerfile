FROM python:2.7.9
MAINTAINER Smári McCarthy <smari@occrp.org>
ENV DEBIAN_FRONTEND noninteractive

RUN echo "deb http://http.us.debian.org/debian stable non-free" >/etc/apt/sources.list.d/nonfree.list
RUN apt-get update -qq && apt-get install -y -q --no-install-recommends \
        curl git python-pip build-essential python-dev libxml2-dev \
        libxslt1-dev apt-utils ca-certificates unrar vim unzip
RUN pip install --upgrade pip && mkdir -p /datasurvey
WORKDIR /datasurvey

COPY requirements.txt /datasurvey/
RUN pip install -r requirements.txt

COPY . /datasurvey/
RUN mkdir -p /var/log/datasurvey/ && pip install -e /datasurvey

CMD ["/bin/bash"]
