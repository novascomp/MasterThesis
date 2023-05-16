FROM python:3.10
WORKDIR /datGen
VOLUME /datgen_vol
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
CMD [ "gunicorn", "--bind" , "0.0.0.0:80", "wsgi:flask_app"]
EXPOSE 80