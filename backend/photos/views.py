import json

from django.http import HttpResponse
from .models import Photo
from .forms import PhotoForm
from engine.object_detection.obj_recog import get_detected_objs
from engine.text_detection.main import get_detected_text
from engine.face_recognition.faceEngine import get_detected_face
from engine.face_recognition.faceEngine import set_detected_face

import os
import asyncio

import sys
sys.path.append("..")


def get_detection(req):
    form = PhotoForm(req.POST, req.FILES)
    if req.method == 'POST':
        res = {}
        image = req.FILES['photo']
        file_name = req.FILES['photo'].name
        new_image = Photo(photo=image)
        new_image.save()

        res["object"] = get_detected_objs(file_name)
        res["face"] = get_detected_face(file_name)
        res["text"] = get_detected_text(file_name)

        # res = get_detected_objs(file_name)
        os.remove('raw/'+file_name)
        return HttpResponse(json.dumps(res), content_type='application/json')


def register_face(req):
    if req.method == 'POST':
        faceName = req.data['name']
        faceList = req.FILE.getlist('faceList')
        faceListName = []
        print(faceList)

        for faceImg in faceList:
            faceListName.append(faceImg.name)
            new_image = Photo(photo=faceImg)
            new_image.save()

        set_detected_face(faceListName)

        for file_name in faceListName:
            os.remove('raw/' + file_name)