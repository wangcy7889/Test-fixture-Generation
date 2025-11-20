FROM continuumio/miniconda3

WORKDIR /app

RUN conda install -y python=3.12.0 && \
    conda clean --all -y

RUN conda init bash && \
    echo "conda activate base" >> ~/.bashrc

CMD ["/bin/bash","--login"]