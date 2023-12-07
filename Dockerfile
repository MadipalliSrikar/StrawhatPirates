FROM python:3.11-alpine
WORKDIR app
COPY . .
RUN apk update && apk add --no-cache linux-headers \
                        python3-dev \
                        gcc \
                        libc-dev
RUN pip install -r requirements.txt
CMD ["python3","app.py"]