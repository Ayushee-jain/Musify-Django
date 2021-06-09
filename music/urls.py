"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index,name='music-home'),

    path('details/<int:album_id>/', views.details,name='music-details'),

    path('songs/', views.songs,name='music-songs'),

    path('<int:album_id>/favorite_album/', views.favorite_album,name='music-favorite-album'),

    path('detail/<int:album_id>/<int:song_id>/favorite/', views.favorite,name='music-favorite'),

    path('<int:song_id>/favorite/', views.song_favorite,name='music-song-favorite'),

    path('album/add', views.AlbumCreate.as_view(template_name='music/add_album.html'),name='music-album-add'),

    path('album/<int:pk>', views.AlbumUpdate.as_view(template_name='music/add_album.html'),name='music-album-update'),

    path('album/<int:pk>/delete/', views.AlbumDelete.as_view(template_name='music/delete_album.html'),name='music-album-delete'),

    path('<int:album_id>/delete/<int:song_id>', views.albumSongDelete,name='music-album-song-delete'),

    path('details/<int:album_id>/song/add/', views.songAdd,name='music-song-add'),

    path('search/',views.search,name='music-search'),

    path('user/', include('users.urls')),
]
