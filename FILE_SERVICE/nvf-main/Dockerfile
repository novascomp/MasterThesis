FROM docker.io/openjdk:11.0.12-jdk-slim
VOLUME /tmp

RUN ls
COPY target/*.jar nvf.jar
EXPOSE 51296

COPY wait-for-it.sh wait-for-it.sh
RUN chmod +x wait-for-it.sh

ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["./wait-for-it.sh owncloud_server:8080 -s -t 300 -- java -jar nvf.jar"]
