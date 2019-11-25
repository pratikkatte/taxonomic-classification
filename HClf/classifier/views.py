from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .start import start_training, predict, train_existing
from django.core.files.storage import FileSystemStorage
from .models import TrainModel
import os

from .forms import predictForm
from .forms import trainForm


@csrf_exempt
def predictView(request):
    form = predictForm()

    if request.method=="POST":
        form = predictForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            model_name = form.cleaned_data['model_name']

            predicted_values = predict(title, description, model_name)
            for q in range(len(predicted_values), 3):
                predicted_values.append(None)

            category, subcategory, subsubcategory = predicted_values

            print("predicted_values", predicted_values)
            return render(request, 'predict.html', {'form':form,
            'title':title, 'description':description, 'model_name':model_name, "category": category, "subcategory":subcategory,
            "subsubcategory":subsubcategory
            })
    return render(request, 'predict.html', {'form':form})


def TrainView(request):
    form = trainForm()

    if request.method=="POST":
        form = trainForm(request.POST, request.FILES)
        if form.is_valid():
            model_name = form.cleaned_data['model_name']
            data_file = request.FILES['data']
            print("uploaded files", data_file.name)
            train_on = form.cleaned_data['train_on']
            fs = FileSystemStorage()
            if fs.exists('data/'+data_file.name):
                os.remove(os.path.join("media/data", data_file.name))

            fs.save('data/'+data_file.name, data_file)
            print(train_on)
            if train_on == 'new_model':

                start_training(data_file.name, model_name)
            else:
                train_existing(data_file.name, model_name, train_on)

            hsvm = TrainModel()
            hsvm.data_name = data_file.name
            hsvm.model_name = model_name+'.model'
            hsvm.save()
            form = trainForm()
            return render(request,  'train.html', {'form':form})
    return render(request, 'train.html', {'form':form})
