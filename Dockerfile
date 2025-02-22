FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /code/src
#COPY ./get_raw_data.py /code/

CMD ["uvicorn", "auth_api.main:app", "--host", "0.0.0.0", "--port", "80"]