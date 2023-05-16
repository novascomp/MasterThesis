FROM debian:stretch-slim
LABEL version="4.50.0.1"
# description= "Utimaco CryptoServer Simulator"
 maintainer = "support@utimaco.com"
ARG SimulatorPort=3001
RUN dpkg --add-architecture i386; \
apt-get update; \
apt-get install -y \
libc6-i386 \
lib32gcc1; \
rm -rf /var/lib/apt/lists/*
WORKDIR /simulator/bin
RUN mkdir -p /etc/utimaco/
RUN mkdir -p /opt/utimaco/bin
RUN mkdir -p /opt/utimaco/lib
RUN chmod -R 777 /opt/utimaco
RUN chmod -R 777 /etc/utimaco
COPY sim5_linux /simulator
RUN chmod u+x ./bl_sim5
ENV SDK_PORT=$SimulatorPort
EXPOSE $SimulatorPort
STOPSIGNAL SIGINT
ENTRYPOINT ["./bl_sim5"]
CMD ["-o","-h"]