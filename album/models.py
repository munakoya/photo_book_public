from accounts.models import CustomUser
from django.db import models

# Create your views here.


class Album(models.Model):
    # アルバムモデル
    # クラス変数
    user = models.ForeignKey(
        CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    # 必ず入力させたい → falseにするとマイグレーション時にselect optionがでる → 2の無視で動くかな？
    photo1 = models.ImageField(
        verbose_name='写真1', blank=True, null=True,)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Album'

    def __str__(self):
        return self.title

# 追加


class MultipleImage(models.Model):
    images = models.FileField()
