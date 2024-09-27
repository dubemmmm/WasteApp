from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from .predict import predict_item
import re

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            image_path = handle_uploaded_file(request.FILES['file'])
            predicted_item, method_recycling = predict_item(image_path)
            steps = re.findall(r'\d+\.\s*(.+?)(?=\d+\.\s*|\Z)', method_recycling, re.DOTALL)
            if predicted_item == "Item was not trained with the model":
                context = {'item': predicted_item}
            else:
            #predicted_item = predict_item(image_path)
                context = {'item':predicted_item, 'steps':steps}
            return render(request, 'app/result.html', context)
    else:
        form = UploadFileForm()
    return render(request, 'app/upload.html', {'form': form})


def handle_uploaded_file(file):
    with open('uploaded_image.jpg', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return 'uploaded_image.jpg'
