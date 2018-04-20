# AnalysisModule

## 실행 환경 세팅

### 필요 프로그램 설치

실행하기 전, celery에 필요한 message broker software인 RabbitMQ를 설치한다.

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
### Django Database Initialize
```bash
python manage.py makemigrations
python manage.py migrate
```
### Web Start

아래의 두 방식을 하나로 합쳐 shell  파일로 구성하는 것이 매우 편하다.
각각 프로그램에 따라 로그가 생성된다.
```bash
nohup sh -- ./run_celery.sh > celery.log &
nohup sh -- ./run_django.sh > django.log &
```

#### run_django.sh
본인이 열어놓은 포트에 맞춰 아래의 Bash Shell에서 PORT 부분을 변경하여 실행한다
```bash
python manage.py runserver 0.0.0.0:PORT
```

#### run_celery.sh
```bash
celery -A AnalysisModule worker -B -l info
```
