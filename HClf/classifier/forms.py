from django import forms
from .models import TrainModel

class predictForm(forms.Form):
    title = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    all_models = TrainModel.objects.all()
    all_model_names = ((model.model_name, model.model_name) for model in all_models)

    model_name = forms.CharField(widget=forms.Select(choices=all_model_names))


class trainForm(forms.Form):
    data = forms.FileField()
    model_name = forms.CharField()
    all_models = TrainModel.objects.all()
    all_model_names = [(model.model_name, model.model_name) for model in all_models]
    all_model_names = [('new model','new model')] + all_model_names

    train_on = forms.CharField(widget=forms.Select(choices=all_model_names))
