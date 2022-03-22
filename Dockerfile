FROM python:3

WORKDIR /usr/src/app

RUN git clone --depth 1 https://github.com/hzeller/rpi-rgb-led-matrix.git --branch master --single-branch  \
    && cd rpi-rgb-led-matrix \
    && make build-python PYTHON=$(which python) \
    && make install-python PYTHON=$(which python)

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

COPY *.py ./
COPY *.json ./

CMD [ "python", "./meeting_matrix.py" ]