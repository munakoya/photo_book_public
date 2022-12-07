from django.shortcuts import render
from urllib import request
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
# ログイン状態でないと継承したviewクラスにアクセスできないっていライブラリ
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
#
import logging
from django.urls import reverse_lazy

from django.views import generic
import album

from .models import Album, MultipleImage
# # InquiryFormのインポート → forms.pyにある
from.forms import AlbumCreateForm

import json

# メール
from django.core.mail import send_mail
def notify(request):
    subject = "題名"
    message = "本文"
    from_email = "muna.sakasakuta@gmail.com"
    recipient_list = [
        "muna.sakasakuta@gmail.com"
    ]
    send_mail(subject, message, from_email, recipient_list)
    return render(request, 'album/index.html')

# ロガーの取得
logger = logging.getLogger(__name__)

# p296


class OnlyYouMixIn(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # URLに埋め込まれた主キーから日記データを1件取得 取得できなかった場合は404エラー
        album = get_object_or_404(Album, pk=self.kwargs['pk'])

        # ログインユーザーと日記の作成ユーザーを比較し、異なればraise_exceptionの設定に従う
        return self.request.user == album.user

# urls.pyファイルから呼び出し
# class クラス名(継承元): → 継承元は自分で作成したクラスやDjangoデフォルトのクラスなどが使われること多い


class IndexView(generic.TemplateView):
    # template_nameは デフォルトviewクラスの変数でテンプレート名を指定する
    # 代表的なオーバーライドするクラス変数やメソッドはp4243
    template_name = "albumApp/index.html"


class AlbumView(LoginRequiredMixin, generic.ListView):
    model = Album
    # ちゃんとどのフォルダのファイルなのかを記述しないと反映されないので注意
    template_name = 'albumApp/album_list.html'

    # 複数モデルを作成した場合に必要？
    context_object_name = 'album_list'

    # 1ページに表示するデータの数
    paginate_by = 10

    # ログインユーザーに紐づいたデータを表示
    def get_queryset(self):
        albums = Album.objects.filter(
            # user = self.request.userでログイン中のユーザーのユーザーインスタンスを取得
            # order_byで作成日時を降順に並び替え → 新しい順に表示される
            user=self.request.user).order_by('-created_at')
        return albums

    def get_json(request):
        album_data = { Album.objects.all() }
        data_to_json = json.dumps(album_data)

        return render(request, 'album_list.html', {'data_to_json':data_to_json})

class AlbumCreateView(LoginRequiredMixin, generic.CreateView):
    # モデルとformの作成
    model = Album
    template_name = 'albumApp/album_create.html'
    form_class = AlbumCreateForm
    success_url = reverse_lazy('album:album_list')


    def form_valid(self, form):
        album = form.save(commit=False)
        album.user = self.request.user
        album.save()
        messages.success(self.request, 'アルバムを作成しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "アルバムの作成に失敗しました。")
        return super().form_invalid(form)


class AlbumDetailView(LoginRequiredMixin, generic.DetailView, OnlyYouMixIn):
    model = Album
    template_name = 'albumApp/album_detail.html'
    # pk関係でちゃんと指定できてないっぽくてエラーでたんで消してみたら解消
    # pk_url_kwarg = 'id'


class AlbumUpdateView(LoginRequiredMixin, generic.UpdateView, OnlyYouMixIn):
    model = Album
    template_name = 'albumApp/album_update.html'
    form_class = AlbumCreateForm

    def get_success_url(self):
        return reverse_lazy('album:album_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, 'アルバムを更新しました。')
        return super().form_valid(form)

    def form_invaid(self, form):
        # シングルとダブルクォートの差
        messages.error(self.request, "アルバムの更新に失敗しました")
        return super().form_invalid(form)


class AlbumDeleteView(LoginRequiredMixin, generic.DeleteView, OnlyYouMixIn):
    model = Album
    template_name: str = 'albumApp/album_delete.html'
    success_url = reverse_lazy('album:album_list')
    context_object_name = 'album_list'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "アルバムを削除しました。")
        return super().delete(request, *args, **kwargs)

# 追加


def upload(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for image in images:
            MultipleImage.objects.create(images=image)
    images = MultipleImage.objects.all()
    return render(request, 'albumApp/test.html', {'images': images})