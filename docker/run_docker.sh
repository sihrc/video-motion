#! /bin/bash
docker build -t video-motion .
docker stop video-motion
docker rm video-motion
docker run -v $(pwd):/video-motion --name {[package}} -dt video-motion bash
docker exec -it video-motion bash
