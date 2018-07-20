FROM debian:stable

RUN apt-get update && \
    apt-get install -y \
	cmake \
	git \
	libopencv-dev \
	python-dev \
	python-opencv \
	python-numpy \
	python-scipy \
	python-matplotlib \
	python-pandas \
	python-pip \
        python-pyaudio \
	python-setuptools \
	wget \
	x11vnc \
	xvfb \
	openssh-server
RUN pip install numpy

WORKDIR /

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD *.py ./

CMD ["python", "microphone.py"]
