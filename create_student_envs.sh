#!/bin/bash
if ! command -v conda &> /dev/null
then
	echo "No conda command. Please initiate conda."
	exit 1
fi
while read -r user
do
	echo $user
	conda create --clone base -n $user -y
done < ulist
