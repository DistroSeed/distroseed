#!/bin/bash
rm -rf env
rm -rf static/*
docker ps -a | grep distroseed|awk '{print $1}' | xargs docker stop $i
docker ps -a | grep distroseed|awk '{print $1}' | xargs docker rm $i