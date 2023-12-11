FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu18.04

LABEL author='Oleh Borysevych'
LABEL email='borysevych.oleh87@gmail.com'
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /app \
    && apt-get update \
    && apt-get install -y build-essential wget ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 libgl1-mesa-glx

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O Miniconda.sh && \
	/bin/bash Miniconda.sh -b -p /opt/conda && \
	rm Miniconda.sh
ENV PATH /opt/conda/bin:$PATH

COPY . /app
WORKDIR /app

RUN conda init bash \
    && . ~/.bashrc \
    && conda env update -n base --file requirements.yaml \
    && echo "conda activate"  >> ~/.bashrc

RUN pip install --upgrade pip \
    && pip install -U openmim \
    && mim install mmengine \
    && mim install "mmcv>=2.0.0" \
    && mim install mmdet \
    && pip install -r requirements.txt \
    && pip install git+https://github.com/cocodataset/panopticapi.git

EXPOSE 80

CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "80"]