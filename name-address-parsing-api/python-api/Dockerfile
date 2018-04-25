FROM python:latest


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev curl autoconf automake libtool pkg-config python-dev git apt-utils 


RUN git clone https://github.com/openvenues/libpostal
WORKDIR ./libpostal
RUN ./bootstrap.sh
RUN ./configure --datadir=/tmp
RUN make
RUN make install

RUN mkdir -p /home/project/python-api
WORKDIR /home/project/python-api
COPY requirements.txt /home/project/python-api
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /home/project/python-api




