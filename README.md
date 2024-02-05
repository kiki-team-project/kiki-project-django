## 프로젝트 소개

keykey 프로젝트는 사용자들이 단축키를 보다 직관적이고 빠르게 이해하고 활용할 수 있도록 돕는것을 목표로하는 애플리케이션입니다. 기존의 단축키 관련 앱이나 웹페이지들이 목록 형태로 단축키를 나열하는 데 그쳤던 것과 달리, keykey앱을 활용하면 키보드를 화면에 직접 띄워 사용자가 검색한 단축키에 해당하는 키가 불이 들어오는 방식으로 사용자의 편의성을 높였습니다.

## 프로젝트 개요

- 목적: 프로젝트는 사용자가 모르는 단축키를 검색할 때 발생하는 정보 과부하 문제를 해결하고자 하며, 단순하고 직관적인 검색창을 통해 필요한 단축키를 빠르게 찾을 수 있고, 이를 통해 검색 과정을 최소화하고 사용자의 업무 효율성을 높이는데 목적.

- 대상 사용자: keykey앱이 제공하는 단축키 툴을 사용하는 유저.

#### keykey 앱의 실제 동작 모습

프로토타입 : https://drive.google.com/drive/folders/1OBth_sd1yOhgIe8vcpPftA00_fW1xVlP?usp=sharing

프로젝트 배포 : https://keykey.vercel.app/pages/home


## 주요 기능

- 회원 가입 및 로그인 : 회원 별로 자신이 북마크한 프로그램, 프로그램의 단축키 정보를 확인할 수 있음. (회원 가입이 완료된 회원은 질문게시판 이용 가능)

- 프로그램별 단축키 정보: 사용자는 회원가입을 하지 않아도 자신이 원하는 프로그램의 단축키 정보를 조회할 수 있음.

- 검색 기능: 사용자는 회원가입을 하지 않아도 자신이 원하는 프로그램의 단축키 정보를 검색할 수 있음.

- 사용자 관리: 사용자 계정 생성, 권한 할당 및 관리 기능.


##  기술 스택
- 프론트엔드: HTML, CSS, JavaScript 

- 백엔드: Django REST framework

- 데이터베이스: Sqlite

- 호스팅/배포: naver cloud

## install 

``` 
> pip install -r requirements.txt
```

## shell script
``` 
> python manage.py makemigrations  
> python manage.py migrate 
> python manage.py load_data (DB에 프로그램 리스트 저장)
> python manage.py load_shortcuts (DB에 프로그램 단축키 데이터 저장)
> python manage.py runserver
```


## 📋 API 명세

https://lumbar-front-60a.notion.site/3ad11bef299b49509ea676171d697012?v=6f58d9f4935540a2acd213dc630906fc&pvs=4
