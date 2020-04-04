FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /apps/
RUN mkdir /apps/vocabtrain
WORKDIR /apps/vocabtrain
COPY requirements.txt /apps/vocabtrain/
RUN pip install -r requirements.txt
COPY vocabtrain /apps/vocabtrain
COPY start_django.sh /apps/vocabtrain
EXPOSE 8080
RUN ["chmod", "+x", "./start_django.sh"]
ENTRYPOINT ["./start_django.sh"]