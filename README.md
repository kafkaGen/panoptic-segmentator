# Panoptic Segmentator

<div id="header" align="center">
  <img src="https://media.giphy.com/media/M9gbBd9nbDrOTu1Mqx/giphy.gif" width="100"/>
</div>

## Introduction

<div id="header" align="center">
  <img src="demo.gif"/>
</div>

Welcome to PanopticSegmentator, a cutting-edge web application that empowers users to perform panoptic segmentation on images, videos, and even live webcam feeds. Panoptic segmentation goes beyond traditional semantic segmentation by not only classifying objects in an image but also distinguishing between stuff (e.g., background) and things (e.g., objects).

## Installation and Usage
To run web aplication you have two option:
- install repository localy with conda:
    - `apt-get install ffmpeg`
    - `git clone https://github.com/kafkaGen/panoptic-segmentator`
    - `conda env create -n <env_name>  --file requirements.yaml`
    - `conda activate <env_name>`
    - `pip install -r requirements.txt`
    - `pip install -U openmim`
    - `mim install mmengine "mmcv>=2.0.0" mmdet git+https://github.com/cocodataset/panopticapi.git`
    - `python setup.py --download-models`
    - `streamlit run streamlit_app.py --server.port 80`
- build or pull docker image (you still need to clone repo to get docker-compose files)
    - `docker build -t panoptic-segmentator .` \
    or
    - `docker pull olko123123123/panoptic-segmentator:latest && docker tag olko123123123/panoptic-segmentator:latest panoptic-segmentator:latest`
    - `bash container-run.sh`

> NOTE: `container-run.sh` automaticaly choose if nvidia-gpu is supported on your machine and run docker container on cpu or gpu version.  

Nevertheless, you can always try on application by this [host](http://54.82.25.5/) - it is AWS EC2 free tier instance, so be patiance to it perfomance :)

## REST API for batch inference

### todo
- model optimization (ONNX, pruning, ...)
- add fastapi, service and client script
- add pytest (test job to ci/cd, pre-commit)