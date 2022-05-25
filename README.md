# DGSB
물체, 텍스트, 사람 등 일반적인 사람이 얻을 수 있는 시각 정보들을 시각 장애인들에게 음성 형태로 전달하는 가이드 서비스

## Dev tech stack
### Engine
- OpenCV
- Tessseract OCR
- Tensorflow
### Backend
- Django
- Django restframework
### MobileApp
- Kotlin
- Android Studio
### DevOps
- Git
- Docker
### Team Collaboration
Notion: <https://www.notion.so/a82b75788d374d658dd19d8fd27d2f56>

## Main features
- 손가락 지칭 기반 텍스트 인식

- 얼굴인식

- 물체인식
Yolo v3기반 물체인식 모듈 개발

## How to run
### Local Server
1. `$ cd backend`
2. `$ python manage.py runserver`

### Docker Container
1. `$ docker pull seyoung8239/dgsb`
2. `$ docker run -p 8000:8000 seyoung8239/dgsb`

## Contribution
### [황태호: ThisIsHwang]
- [PM] Project Managing (Agile, Scrum)
- [Engine] Face Recognition

### [권재현: KwonJaeH]
- [Engine] Finger pointing based text recognition
- [Paper] Project paper

### [박세영: seyoung8239]
- [Engine] Object Recognition
- [Server] Server with Django
- [DevOps] Deployment server (Docker, AWS EC2)
- [Docs] Documentation

### [황하연]
- [Client] Mobile application
- [DevOps] Deployment application on android market
