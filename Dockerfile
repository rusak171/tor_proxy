FROM debian:latest
RUN apt-get update
ADD . /code
WORKDIR /code
RUN apt-get install -y tor curl
COPY torrc /etc/tor/torrc
RUN apt-get install -y python3 && apt-get install -y python3-pip
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt 
CMD ["/bin/bash", "cmd.sh"]
# CMD service tor start && sleep 2 && python3 change_toridentity.py
# CMD service tor start && sleep 2 && curl --proxy socks5h://127.0.0.1:9050 https://check.torproject.org/api/ip && sleep 300