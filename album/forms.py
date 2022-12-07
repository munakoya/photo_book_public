import os
from django import forms
# メール送信を簡単に行うdjangoの関数
from django.core.mail import EmailMessage

from album.models import Album


class AlbumCreateForm(forms.ModelForm):
    class Meta:
        model = Album
        # 一時的にphoto2消します
        fields = ('title', 'photo1', 'photo2', 'photo3')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
