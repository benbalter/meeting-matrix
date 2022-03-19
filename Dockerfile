FROM python:3

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y git make build-essential \
    python3-dev python3 python3-distutils libsdl2-dev python3-pillow

RUN git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3)

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./meeting_matrix.py" ]
