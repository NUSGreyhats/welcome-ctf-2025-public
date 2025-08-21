#!/bin/bash

#script to recursively travel a dir of n levels

function traverse() {
curr=`pwd`
for file in "$1"/*
do
    if [ ! -d "${file}" ] ; then
	    if [[ ${file} =~ (compose.yml|compose.yaml|docker-compose.yml|docker-compose.yaml) ]]; then
		dockerdir=`dirname $file`
		challname=`basename $dockerdir`
		cd $dockerdir
		if [[ $challname =~ (service|source) ]]; then
			challname=`basename \`dirname $dockerdir\``
		fi
		if [[ ! `basename $dockerdir` =~ "dist" ]] && [[ ! $dockerdir =~ "finals" ]] && [[ ! $challname =~ (Example|lpmc) ]]; then
			echo "bringing up $challname"
			sudo docker-compose down -v --rmi all --remove-orphans
		fi
		cd $curr
	fi
    else
        traverse "${file}"
    fi
done
}

function main() {
    traverse "$1"
}

main "$1"

