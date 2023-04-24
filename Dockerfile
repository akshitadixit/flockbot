# dockerfile to run sanic app on ec2
FROM python:3.10
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-pip \
    nginx

# # run nginx using config file
# RUN rm /etc/nginx/sites-enabled/default
# COPY nginx.conf /etc/nginx/sites-enabled/
# RUN service nginx start

# copy app files
COPY . .

# set working directory
WORKDIR /

# install python dependencies
RUN pip3 install -r requirements.txt

# expose port
EXPOSE 8000

# run app
CMD ["python3", "index.py"]

