# Thanks to https://github.com/nuveo/docker-opencv
FROM jjanzic/docker-python3-opencv

LABEL author="Chris Lee"
LABEL email="sihrc.c.lee@gmail.com"

ENV PATH=/video-motion/bin:${PATH} PYTHONPATH=/usr/local/lib/python3.6/site-packages:${PYTHONPATH}

COPY requirements.txt /requirements.txt

RUN apt-get update && \
    pip3 install --upgrade pip wheel && \
    pip3 install -r requirements.txt


COPY . /video-motion
WORKDIR /video-motion

RUN python3 setup.py develop

CMD ["bash"]