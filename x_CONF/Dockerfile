FROM debian:stretch-slim

COPY p11tool2 ./
COPY ADMIN.key ./
COPY libcs_pkcs11_R3.so ./
COPY cs_pkcs11_R3.cfg ./
COPY wait-for-it.sh ./

RUN chmod 777 ./p11tool2
RUN chmod u+x ./p11tool2
ENTRYPOINT [ "/bin/bash", "-c" ]
CMD ["sleep 15s; ./p11tool2 Label=$PKCS11_TOKEN_NAME Login=ADMIN,./ADMIN.key InitToken=$SO_PIN; ./p11tool2 LoginSO=$SO_PIN InitPIN=$USER_PIN"]