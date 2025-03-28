#!/bin/bash

sudo docker system prune 
sudo docker compose -f docker/docker-compose.prod.yml --env-file .env up --build 

