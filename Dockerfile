# Have tested with a custom Ubuntu-1804 / Python 3.7 / Tensorflow 2.6.2 Base Image
# Not tested with this image. 
# docker run -v /home/celso/work:/work -v /mnt/datasets:/datasets -v /data:/data -v /mnt/datasets/tensorflow_datasets:/home/jax/tensorflow_datasets -it --rm --gpus device=0 -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix meshtransformerjax_tf:latest bash
FROM nvcr.io/nvidia/tensorflow:21.04-tf2-py3


RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    cmake \
    wget \
    git \
    unzip \
    software-properties-common \
    apt-utils \
    ffmpeg \
    libsm6 \
    libxext6 
    

RUN python -m pip install --upgrade pip

RUN pip install torch==1.10.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html 

# you probably want to create a new user as an entry point, not run root inside the container
ENV TF_FORCE_GPU_ALLOW_GROWTH='true'
# install python packages via pip
# for CUDA support, we have to specify a particular jaxlib version
# we also need to specify the particular cuda version

RUN git clone https://github.com/celsopitta/mesh-transformer-jax.git 
RUN pip install -r mesh-transformer-jax/requirements.txt 
RUN pip install jax[gpu]==0.2.16
RUN pip install requests

ENV PYTHONPATH /usr/local/bin/python3
ENV PATH $PYTHONPATH:$PATH
ENV TOKENIZERS_PARALLELISM=true

CMD /bin/bash




