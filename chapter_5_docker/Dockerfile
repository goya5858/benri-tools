FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY ./ /app
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--port", "8000", "--reload"]