FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ Asia/Shanghai
WORKDIR /app
COPY * ./
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt update \
    && apt install -y python3 python3-pip \
    && apt install -y tesseract-ocr \
    && pip3 install -r ./requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && cp ./num.traineddata /usr/share/tesseract-ocr/4.00/tessdata/num.traineddata \
    && apt-get purge -y --auto-remove
