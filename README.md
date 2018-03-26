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
### Django App 
본인이 열어놓은 포트에 맞춰 아래의 Bash Shell에서 PROT 부분을 변경하여 실행한다
```bash
python manage.py runserver 0.0.0.0:PORT
```

