FROM python:3

WORKDIR /usr/src/app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install -y git make build-essential \
    python3-dev python3 python3-distutils libsdl2-dev python3-pillow \
    python3-numpy python3-pip python3-wheel python3-setuptools 

RUN git clone https://github.com/hzeller/rpi-rgb-led-matrix.git \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python3) \
    && make install-python PYTHON=$(which python3)

RUN pip3 install --upgrade pip setuptools wheel                                                                                                                                                                                                
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./meeting_matrix.py" ]
