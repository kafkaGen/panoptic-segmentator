FROM python:3.10.10-slim

LABEL author='Oleh Borysevych'
LABEL email='borysevych.oleh87@gmail.com'

RUN mkdir /app
RUN apt-get update \
    && apt-get install -y wget ffmpeg libsm6 libxext6 \
    && wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/root/miniconda3/bin:$PATH"
RUN mkdir /root/.conda && bash Miniconda3-latest-Linux-x86_64.sh -b

COPY streamlit_app.py requirements.txt requirements.yaml docker-compose.yml /app/
COPY core /app/core
COPY models /app/models
COPY settings /app/settings
WORKDIR /app

RUN conda init bash \
    && . ~/.bashrc \
    && conda env create -f requirements.yaml \
    && conda activate panoptic-segmentator \
    && pip install --upgrade pip
RUN pip install -U openmim
RUN mim install mmengine
RUN mim install "mmcv>=2.0.0"
RUN mim install mmdet
RUN pip install -r requirements.txt


EXPOSE 80

CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "80"]