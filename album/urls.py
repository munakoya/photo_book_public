from django.conf.urls.static import static
from django.conf import settings
from distutils.command.upload import upload
from django.urls import path
from.import views

app_name = 'album'

urlpatterns = [
    # indexページ
    path('', views.IndexView.as_view(), name="index"),
    # albumページの作成
    path('album_list/', views.AlbumView.as_view(), name="album_list"),
    # アルバム新規作成
    path('album_create/', views.AlbumCreateView.as_view(), name="album_create"),
    # アルバム詳細ページ
    path('album_detail/<int:pk>/',
         views.AlbumDetailView.as_view(), name="album_detail"),

    # アルバム更新機能
    path('album_update/<int:pk>',
         views.AlbumUpdateView.as_view(), name="album_update"),
    # アルバム削除機能
    path('album_delete/<int:pk>',
         views.AlbumDeleteView.as_view(), name="album_delete"),

    # 追加
    path('view', views.upload, name='upload'),
]
