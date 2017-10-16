FROM ubuntu:16.04

LABEL maintainer="tjelvar.olsson@jic.ac.uk"

RUN apt-get update && apt-get install -y  \
    python-pip  \
    python-tk  \
    wget  \
    libfuse2
RUN pip install --upgrade pip
RUN pip install "dtool==2.2.0"
RUN wget ftp://ftp.renci.org/pub/irods/releases/4.1.10/ubuntu14/irods-icommands-4.1.10-ubuntu14-x86_64.deb
RUN dpkg -i irods-icommands-4.1.10-ubuntu14-x86_64.deb
RUN apt-get install -f -y 
RUN rm -rf /var/lib/apt/lists/* irods-icommands-4.1.10-ubuntu14-x86_64.deb
