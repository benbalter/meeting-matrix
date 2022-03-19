FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y git make build-essential \
    python3-dev python3 python3-distutils libsdl2-dev python3-pillow \
    python3-numpy

RUN git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3)

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./meeting_matrix.py" ]
