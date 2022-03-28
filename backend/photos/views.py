from django.http import HttpResponse
from .models import Photo
from .forms import PhotoForm
from

def get_detection(req):
    form = PhotoForm(req.POST, req.FILES)
    if req.method == 'POST':
        if form.is_valid():
            image = req.FILES['photo']
            new_image = Photo(photo=image)
            print(new_image)

            # new_image.save()
            # return HttpResponse(json.dumps(response_data), mimetype='application/json')