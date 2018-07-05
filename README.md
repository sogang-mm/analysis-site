# Analysis Site

- [Introduce](#introduce)
- [Installation](#installation)
    - [From Source](#from-source)
    - [Docker Compose](#docker-compose)
- [Setting Database](#setting-database)
    - [Make Database](#make-database)
    - [Edit Database](#edit-database)
- [Create Administrator Account](#create-administrator-account)
- [Run Web Server](#run-web-server)
- [Registration Module and Group](#registration-module-and-group)
    
## Introduce

본 프로젝트는 Neural Network의 결과를 REST API로 서비스 하기 위한 웹 서버를 제공합니다.

본 프로젝트는 [Analysis Module](https://github.com/sogang-mm/Analysis-Module)로 구성된 여러 Module을 한 번에 관리하기 위해 진행되었습니다.

따라서 본 프로젝트를 사용하고자 한다면 먼저 [Analysis Module](https://github.com/sogang-mm/Analysis-Module)로 부터 Module에 따른 프로젝트를 진행하시기 바랍니다.

Python 코드로 구성되어 있으며, Django 및 Django REST framework를 사용하여 개발하였습니다.

Linux 사용을 가정하여 코드를 작성하였으며, 만약 다른 환경에서의 설치를 진행하려면 문의하시기 바랍니다.


## Installation

### From Source

실행에 필요한 service를 설치한다.
```bash
sudo apt-get install postgresql postgresql-contrib rabbitmq-server
sudo service postgresql rabbitmq-server restart
```

실행에 필요한 package를 설치한다.
```bash
pip install -r requirements.txt
```

만약 package 설치가 진행되지 않는다면 pip를 업데이트 한 후 다시 시도한다.
```bash
pip install --upgrade pip
pip install setuptools
```

### Docker Compose

Docker Compose를 사용하기 위해서는 다음을 필요로 한다.

- [Docker](https://docs.docker.com/) & [Docker compose](https://docs.docker.com/compose/)

이후, docker 디렉토리 내 파일에서 다음과 같은 부분을 수정한다.

1. Dockerfile
    * 본인이 사용할 Docker image로 수정한다.
    ```dockerfile
    FROM ubuntu:16.04
    ```
    * 본인의 git repository로 주소를 수정한다. 
    ```dockerfile
    RUN git clone https://github.com/sogang-mm/Analysis-Site.git
    ```
        
2. .env
    * Docker로 여러 Module 을 올리고자 한다면 다음을 수정한다.
    ```text
    COMPOSE_PROJECT_NAME=analysis-site
    WEB_CONTAINER_NAME=site
    WEB_EXTERNAL_PORT=8000
    ```    
    * COMPOSE_PROJECT_NAME은 Dockerfile에서 build한 image의 이름으로 설정된다.
    * WEB_CONTAINER_NAME은 Dockerfile에서 build한 image의 container의 이름으로 설정된다.
    * WEB_EXTERNAL_PORT는 웹 서버의 외부 통신을 위한 PORT로 설정된다.
    
3. env_files/django.env
    * Django의 관리자 계정의 ID와 Password를 변경하려면 다음을 수정한다.
    ```text
    DJANGO_SUPERUSER_USERNAME=root
    DJANGO_SUPERUSER_EMAIL=none@none.com
    DJANGO_SUPERUSER_PASSWORD=password
    ```
    * DJANGO_SUPERUSER_USERNAME는 관리자 계정의 ID를 의미한다. 
    * DJANGO_SUPERUSER_EMAIL는 관리자 계정의 EMAIL를 의미한다. (Optional)
    * DJANGO_SUPERUSER_PASSWORD는 관리자 계정의 Password를 의미한다.

모든 설정이 끝났다면 docker 디렉토리 내에서 docker-compose up으로 실행하면 웹 서버가 시작된다.

http://localhost:8000/ 또는 구성한 서버의 IP 및 Domain으로 접근하여 접속이 되는지 확인한다.

Docker-compse 사용 시 아래 부분을 넘기고 [Registration Module and Group](#registration-module-and-group)부터 진행한다. 


## Setting Database

### Make Database

본 프로젝트에서는 RDBMS로 PostgreSQL을 사용하므로, postgres 계정으로 이동 후 psql을 실행한다.
```bash
sudo su - postgres
psql
```

Django에서 사용할 Database 및 계정을 만들어준다.
```postgresql
CREATE USER site_admin WITH PASSWORD 'site_admin';
CREATE DATABASE site_db;
grant all privileges on database site_db to site_admin;
ALTER ROLE site_admin SET client_encoding TO 'utf-8';
\q
```

설정을 완료했다면 postgres 계정을 logout 한다.
```bash
logtout
```

Django에서 설정한 model 구조를 PostgreSQL의 Database에 반영한다.
```
sh run_migration.sh
```

### Edit Database 

만약 Django 내 model 구조를 변경하고자 한다면, 이전 Database 구조를 삭제하고 다시 만들어주어야 한다. 이를 위해 postgres 계정으로 이동한 뒤 psql을 실행한 후 다음과 같이 진행한다.
```postgresql
DROP DATABASE site_db;
CREATE DATABASE site_db;
grant all privileges on database site_db to site_admin;
\q
```
이후에 다시 migration을 진행한다.

## Create Administrator Account
Module 및 Module Group을 등록하기 위해서는 Web Server의 관리자 계정을 만들어야 한다.
```bash
python manage.py createsuperuser
```

## Run Web Server
* Web Server를 실행하고자 한다면 server_start.sh를 실행한다.
    ```bash
    sh server_start.sh
    ```
    이후 http://localhost:8000/ 또는 구성한 서버의 IP 및 Domain으로 접근하여 접속한다.

* 만약 접속 시 문제가 있어 실행 Log를 보고자 할 때는 다음과 같이 실행하여 확인한다.
    * Web Server에 문제가 있어 Django 부분만 실행하고자 한다면 run_django.sh를 실행한다.
        ```bash
        sh run_django.sh
        ```
    
    * Web Server는 실행되나 Analysis-Module로 구성한 Web Server로부터 결과가 나오지 않는다면 run_celery.sh를 실행한다.
        ```bash
        sh run_celery.sh
        ```
    
* Web Server를 종료하고자 한다면 server_shutdown.sh를 실행한다.
    ```bash
    sh server_shutdown.sh
    ``` 

## Registration Module and Group

실행 이후 모듈을 등록하기 위해 관리자 페이지에 접속한다.

만약 local에서 작업하였다면, http://localhost:8000/admin 으로 접속하여 만든 관리자 계정으로 로그인하여 Module 및 Group을 추가한다.
 