FROM ubuntu:22.04

ENV user ctf

RUN apt-get -y update
RUN apt-get install -y python3 socat && rm -rf /var/lib/apt/lists/*

RUN useradd $user
WORKDIR /home/$user

COPY ./sunshinefactory /home/$user/sunshinefactory
COPY ./flag.txt /home/$user/flag.txt
RUN chmod +x sunshinefactory
RUN chmod 644 flag.txt

USER $user

CMD socat TCP-LISTEN:33001,reuseaddr,fork EXEC:/home/$user/sunshinefactory,stderr