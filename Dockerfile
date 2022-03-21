FROM python:3

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y git make build-essential \
    python3-dev python3 python3-distutils libsdl2-dev python3-pillow \
    python3-numpy python3-pip python3-wheel python3-setuptools python3-pygame

RUN apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev libjpeg-dev python3-setuptools python3-dev python3-numpy python3-scipy python3-pygame

RUN git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3)

RUN python3 -m pip install --upgrade pip setuptools wheel                                                                                                                                                                                                
COPY requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD [ "python3", "./meeting_matrix.py" ]
