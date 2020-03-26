FROM ubuntu

RUN apt-get update \
    && apt-get install -y git python3-pip python3.6 \
    && apt-get install -y openslide-tools vim

COPY ./*.py /opt/
COPY requirements.txt /opt/

COPY ./images.sh /usr/bin/images
RUN chmod 0755 /usr/bin/images
COPY ./annotations.sh /usr/bin/annotations
RUN chmod 0755 /usr/bin/annotations

RUN cd /opt \
    && pip3 install -r /opt/requirements.txt

COPY run.sh /tmp/run.sh
RUN chmod 755 /tmp/run.sh

CMD ["sh", "/tmp/run.sh"]