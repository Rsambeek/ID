FROM python:3.6-slim

WORKDIR /app

ADD . /app

#RUN dpkg -i libssl1.1_1.1.0f-3+deb9u1_armel.deb
#RUN dpkg -i libpython3.5-minimal_3.5.3-1_armel.deb
#RUN dpkg -i python3.5-minimal_3.5.3-1_armel.deb
#RUN dpkg -i python3-minimal_3.5.3-1_armel.deb
#RUN dpkg -i libtinfo5_6.0+20161126-1+deb9u1_armel.deb
#RUN dpkg -i libncursesw5_6.0+20161126-1+deb9u1_armel.deb
#RUN dpkg -i libmpdec2_2.4.2-1_armel.deb
#RUN dpkg -i libreadline7_7.0-3_armel.deb
#RUN dpkg -i mime-support_3.60_all.deb
#RUN dpkg -i libpython3.5-stdlib_3.5.3-1_armel.deb
#RUN dpkg -i libpython3-stdlib_3.5.3-1_armel.deb
#RUN dpkg -i python3.5_3.5.3-1_armel.deb
#RUN dpkg -i python3_3.5.3-1_armel.deb dh-python_2.20170125_all.deb
#RUN dpkg -i libpython3.5_3.5.3-1_armel.deb
#RUN dpkg -i dietlibc-dev_0.34~cvs20160606-6_armel.deb
#RUN dpkg -i linux-libc-dev_4.9.65-3+deb9u2_armel.deb
#RUN dpkg -i libc6_2.24-11+deb9u1_armel.deb
#RUN dpkg -i libc-dev-bin_2.24-11+deb9u1_armel.deb
#RUN dpkg -i libc6-dev_2.24-11+deb9u1_armel.deb
#RUN dpkg -i libexpat1_2.2.0-2+deb9u1_armel.deb
#RUN dpkg -i libexpat1-dev_2.2.0-2+deb9u1_armel.deb
#RUN dpkg -i libpython3.5-dev_3.5.3-1_armel.deb
#RUN dpkg -i python3.5-dev_3.5.3-1_armel.deb
#RUN dpkg -i libpython3-dev_3.5.3-1_armel.deb
#RUN dpkg -i python3-dev_3.5.3-1_armel.deb
#RUN dpkg -i libevent-2.0-5_2.0.21-stable-3_armel.deb
#RUN dpkg -i libevent-core-2.0-5_2.0.21-stable-3_armel.deb
#RUN dpkg -i libevent-extra-2.0-5_2.0.21-stable-3_armel.deb
#RUN dpkg -i libevent-openssl-2.0-5_2.0.21-stable-3_armel.deb
#RUN dpkg -i libevent-pthreads-2.0-5_2.0.21-stable-3_armel.deb
#RUN dpkg -i libevent-dev_2.0.21-stable-3_armel.deb
#RUN python3 setup.py install

RUN pip3 install -U setuptools
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --egg -r requirements.txt

CMD ["python", "gatekeeper.py"]
