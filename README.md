# DGSB
물체, 텍스트, 사람 등 일반적인 사람이 얻을 수 있는 시각 정보들을 시각 장애인들에게 음성 형태로 전달하는 가이드 서비스
## Dev 기술스택

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

## How to Run
### Local Server
1. `$ cd voteSite`
2. `$ python manage.py runserver`

### Docker Container
1. `$ docker pull seyoung8239/boat-vote-be`
2. `$ docker run -p 8000:8000 seyoung8239/boat-vote-be`

## API docs
We used a OpenDocs3.0 based `Swagger API`. You can access docs with the below path after run a server

`http://0.0.0.0:8000/swagger/` 

`http://0.0.0.0:8000/redoc/`

## Contribution
### [남도하]

### [박세영]
- JWT 도입
- OpenDocs3.0 Swagger API 도입
- Docker image 관리
- AWS EC2로 배포

### [오영선]
