FROM ubuntu:22.04 AS app

FROM pwn.red/jail

COPY --from=app / /srv
COPY ./mchall /srv/app/run
COPY ./flag.txt /srv/app/flag.txt

RUN rm /srv/bin/more /srv/bin/head /srv/bin/tail /srv/bin/tac /srv/bin/sed /srv/bin/awk /srv/bin/cat
