# DGSB
Guide service that delivers visual information that can be obtained by ordinary people, such as objects, text, and people, in voice form to the visually impaired  
### Team Collaboration
Notion: <https://www.notion.so/a82b75788d374d658dd19d8fd27d2f56>

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

## Main features
### Finger pointing-based text recognition
- Image preprocessing for text recognition  
- Checking the presence of text in pointing direction  
### Face recognition
- Cropping Faces from Images using OpenCV
- Face recognition using Haar Algorithm
- Register faces with cropped face images 
- Get face features using Histogram of Gradient (HoG)  
### Object recognition 
- Development of an Object Identification Module Based on Yolo v3  
- 
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
