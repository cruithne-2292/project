# build on a base image 
FROM python:3.7.12

# install database server
RUN apt-get --yes update && apt-cache search mysql-server && apt-get --yes install mariadb-server vim cron build-essential cmake pkg-config libx11-dev libatlas-base-dev libgtk-3-dev libboost-python-dev

# copy the requirements
COPY requirements.txt ./
# install python dependencies
RUN pip install --upgrade --no-cache-dir pip
RUN pip install --no-cache-dir -r requirements.txt

# for gunicorn logging
RUN mkdir /var/log/gunicorn
# set project directory as default
WORKDIR /usr/src/project
# copy project files to the /usr/src/project folder
ADD . /usr/src/project

# expose ports
EXPOSE 8080

# set entrypoint
ENTRYPOINT ["/bin/bash", "/usr/src/project/scripts/entrypoint.sh"]
