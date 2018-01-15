# tigereye API SERVER

FROM registry.wepiao.com/pypy2app:v1
MAINTAINER Gu Ye <guye@wepiao.com>

LABEL description="tigereye API SERVER"
RUN echo "Asia/Shanghai" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
COPY etc/config.py /usr/src/app/config.py
ENV tigereye_SETTINGS=/usr/src/app/config.py
EXPOSE 5000
CMD ["gunicorn", "-b0.0.0.0:5000", "-w8", "wsgi:tigereye"]
