### 1. Get Linux
FROM andreper/jupyterlab:3.0.0-spark-3.0.0

WORKDIR /pkcs11
VOLUME /pkcs11_vol
COPY . .

RUN apt-get install wget
RUN pip3.9 install --trusted-host pypi.python.org -r requirements.txt
RUN pip3.9 install --trusted-host pypi.python.org gunicorn
ENV PKCS11_MODULE=/pkcs11/libcs_pkcs11_R3.so
ENV CS_PKCS11_R3_CFG=/pkcs11/cs_pkcs11_R3.cfg
#ENV JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"
CMD [ "gunicorn", "--bind" , "0.0.0.0:80", "wsgi:flask_app"]
EXPOSE 80
#https://stackoverflow.com/questions/55549964/permission-error-permission-denied-in-simple-basic-flask-application