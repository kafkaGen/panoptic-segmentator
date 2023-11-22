FROM mambaorg/micromamba

LABEL author='Oleh Borysevych'
LABEL email='borysevych.oleh87@gmail.com'

COPY --chown=$MAMBA_USER:$MAMBA_USER requirements.yaml /tmp/env.yaml
RUN micromamba install -y -n base -f /tmp/env.yaml && \
    micromamba clean --all --yes

# RUN apt update
RUN mkdir app

COPY streamlit_app.py requirements.yaml docker-compose.yml /app/
COPY core /app/core
WORKDIR /app

EXPOSE 80

CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "80"]