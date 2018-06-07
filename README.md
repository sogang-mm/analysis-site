# AnalysisModule

## 실행 환경 세팅

### 필요 프로그램 설치

#### 일반적인 사용 시

본 프로젝트는 RDBMS로 PostgreSQL을 사용하므로, PostgreSQL를 설치한다.

```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql restart
```

실행하기 전, Celery에 필요한 message broker software인 RabbitMQ를 설치한다.

```bash
sudo apt-get install rabbitmq-server
sudo service rabbitmq-server restart
```

이후 필요한 pip package를 설치한다
```bash
pip install -r requirements.txt
```

만약 pip requirements가 설치되지 않는다면 pip를 업데이트 한 후, 다음 package를 먼저 설치한다
```bash
pip install --upgrade pip
pip install setuptools
```

#### Docker 사용 시

Docker를 사용할 경우 docker 폴더로 이동하여 Dockerfile의 맨 윗부분의 FROM 부분을 본인이 사용할 Docker Image로 수정하고 빌드한다.

##### Dockerfile
```Dockerfile
FROM ubuntu:16.04
```

##### Docker Build
```bash
cd docker
docker build [OPTIONS] -t [TAG] .
```


## Database 설정하기

### 만들기

PostgreSQL를 사용하기 위해 postgres 계정으로 이동한 후 psql을 실행한다.
```bash
sudo su - postgres
psql
```

Django에서 사용할 Database를 만들고 설정을 진행한다.
```bash
CREATE USER site_admin WITH PASSWORD 'site_admin';
CREATE DATABASE site_db;
grant all privileges on database site_db to site_admin;
ALTER ROLE site_admin SET client_encoding TO 'utf-8';
ALTER ROLE site_admin SET timezone TO 'Asia/Seoul';
\q
```

설정이 모두 끝났으면 postgres 계정에서 logout 한다.
```bash
logout
```

Django 내에서 설정한 model 구조를 PostgreSQL의 Database에 반영한다.
```bash
sh initailize_server.sh
```


### 수정하기

이 과정은 Django 내의 model 구조가 바뀔 때 마다 다시 만들어주어야 한다 한다.
위의 만들기 과정에서 psql을 실행한 후의 부분을 아래와 같이 Database를 삭제 및 다시 생성하는 과정을 진행한다. 그 이후에는 같은 방식으로 진행한다.
```bash
DROP DATABASE site_db;
CREATE DATABASE site_db;
grant all privileges on database site_db to site_admin;
\q
```



## 실행하기

### Superuser 만들기
Module 및 Module Group을 등록하기 위해서는 superuser이 필요하다.
```bash
python manage.py createsuperuser
```

### Web Start
전체 과정을 실행하는 것은 다음과 같이 입력한다.
```bash
sh start_server.sh
```

#### Django Only
만약 Debug 등의 이유로 Django만 실행하고 싶을 경우 다음과 같이 입력한다. 주로 웹 페이지를 통한 접근에 문제가 있을 경우, 확인을 위해 실행한다.
```bash
sh run_django.sh
```

#### Celery Only
만약 Debug 등의 이유로 Celery만 실행하고 싶을 경우 다음과 같이 입력한다. 주로 Module을 통한 결과에 문제가 있을 경우, 확인을 위해 실행한다.
```bash
sh run_celery.sh
```

### Web Shutdown
전체 프로그램을 종료하는 것은 다음과 같이 입력한다.
```bash
sh shutdown_server.sh
```
