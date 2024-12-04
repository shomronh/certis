FROM python
RUN mkdir /certis
RUN chmod 777 /certis
COPY . /certis
WORKDIR /certis

RUN pip install -r requirements.txt
CMD ["python","certis_app.py"]



