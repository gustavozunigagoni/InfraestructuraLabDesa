FROM python:3.11.8-slim

ARG SSH_PASSWORD

USER root

WORKDIR /app

RUN apt-get update
RUN apt-get install -y openssh-server curl apt-transport-https
RUN mkdir /var/run/sshd
RUN echo "root:${SSH_PASSWORD}" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/^mesg n$/tty -s \&\& mesg n/g' /root/.profile

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 22 8501

CMD ["/usr/sbin/sshd", "-D"]


