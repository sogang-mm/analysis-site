# AnalysisModule

## 실행 환경 세팅

### 필요 프로그램 설치

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



#### 일반적인 사용 시

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


### Django Secret Key

Django 실행에 필요한 Secret Key를 구성한다.
```bash
cd AnalysisModule
vi secret_key.py
``` 
- secret_key.py
```python
SECRET_KEY = ""
```


## 실행하기
### Django Initialize
해당 프로그램을 실행하기 위해서는 Django에서 Database를 초기화해야 한다.
이 작업은 맨 처음 및 Django의 Model 구조 변화 시 필요하다.
```bash
sh initailize_server.sh
```

### Web Start
전체 프로그램을 실행하는 것은 다음과 같이 입력한다.
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
