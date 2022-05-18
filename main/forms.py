from django import forms
from django.utils.safestring import mark_safe
from bootstrap_modal_forms.forms import BSModalForm
from main.models import *
from simplecaptcha import captcha

class NewVideoForm(forms.Form):
    title = forms.CharField(label=' Video Title', max_length=25)
    description = forms.CharField(
        label='Video Description', max_length=300,
        widget=forms.Textarea(
        attrs={
            'class': 'form-control', 'rows': 4}))
    file = forms.FileField()

@captcha
class CNewVideoForm(forms.Form):
    title = forms.CharField(label=' Video Title', max_length=20)
    description = forms.CharField(
        label='Video Description', max_length=300,
        widget=forms.Textarea(
        attrs={
            'placeholder': 'Video Description',
            'class': 'form-control', 'rows': 4}))
    file = forms.FileField()


class NewYTVideoForm(forms.Form):
    link = forms.CharField(label=' Link', max_length=100)
    # title = forms.CharField(label=' Video Title', max_length=20)
    # description = forms.CharField(label='Video Description', max_length=300)

@captcha
class CNewYTVideoForm(forms.Form):
    link = forms.CharField(label=' Link', max_length=100)
    # title = forms.CharField(label=' Video Title', max_length=20)
    # description = forms.CharField(label='Video Description', max_length=300)

class ChannelForm(forms.Form):
    profilepic = forms.CharField(max_length=50, label='Channel Name')
    # username = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # suscribers = models.IntegerField(default=0, blank=False, null=False)

class ChangePP(forms.Form):
    profilepic = forms.FileField()

class MyForm(forms.Form):
    searchindesc = forms.BooleanField(required=False)
    searchintitle = forms.BooleanField(required=False)

