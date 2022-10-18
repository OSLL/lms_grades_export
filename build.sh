#!/bin/bash

#Builds image 

dir=${1}
docker build -t ${dir}_parser ${dir}/.
