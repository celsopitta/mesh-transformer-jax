# Have tested with a custom Ubuntu-1804 / Python 3.7 / Tensorflow 2.6.2 Base Image
# Not tested with this image. 
FROM tensorflow/tensorflow:2.6.0
RUN apt update && \
    apt-get install git -y

WORKDIR /app/
COPY . /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN git clone https://github.com/celsopitta/mesh-transformer-jax.git 
RUN pip install torch==1.10.0
RUN pip install -r mesh-transformer-jax/requirements.txt 
RUN pip install mesh-transformer-jax/ jax==0.2.12
RUN pip install fastapi uvicorn requests aiofiles aiohttp 
RUN ln -s /app/start.sh /start.sh

ENV PYTHONPATH /app:/app/mesh-transformer-jax:/usr/local/bin/python3
ENV PATH $PYTHONPATH:$PATH
ENV TOKENIZERS_PARALLELISM=true
EXPOSE 80

#CMD ["/start.sh"]

CMD /bin/bash

