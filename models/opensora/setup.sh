#!/bin/bash

cd ~
git clone https://github.com/hpcaitech/Open-Sora.git
cd Open-Sora
sudo docker build -t opensora -f ~/image-eval/models/opensora1.2/Dockerfile .