FROM ubuntu:22.04

ENV user ctf

RUN apt-get -y update
RUN apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

RUN useradd $user
WORKDIR /home/$user

COPY ./chall.py /home/$user/chall.py
COPY ./flag.txt /home/$user/flag.txt
RUN chmod +x chall.py

CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/home/$user/chall.py,stderr
