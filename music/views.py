from django.http.response import HttpResponse, JsonResponse
from music.forms import SongForm
from django.http import request
from django.shortcuts import get_object_or_404, redirect, render
from .models import Album, Song
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse

AUDIO_FILE_TYPES = ['wav', 'mp3', 'mp4', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

def index(request):
    all_album=Album.objects.all()
    return render(request,'music/index.html',{'all_album':all_album})

def details(request,album_id):
    album=get_object_or_404(Album,pk=album_id)
    all_songs=album.song_set.all()
    return render(request,'music/details.html',{'all_songs':all_songs,'album':album})

def favorite_album(request,album_id):
    album=get_object_or_404(Album,pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite=False
            album.save()
        else:
            album.is_favorite=True
            album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return redirect('music-home')

def favorite(request,album_id,song_id):
    song=get_object_or_404(Song,pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite=False
            song.save()
        else:
            song.is_favorite=True
            song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return redirect('/music/details/'+str(album_id)+'/')

def song_favorite(request,song_id):
    song=get_object_or_404(Song,pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite=False
            song.save()
        else:
            song.is_favorite=True
            song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success':False})
    else:
        return redirect('music-songs')

def songs(request):
    all_songs=[]
    for alb in Album.objects.all():
        for song in alb.song_set.all():
            all_songs.append(song)
    return render(request,'music/songs.html',{'all_songs':all_songs})

def songAdd(request,album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                return render(request, 'music/add_song.html', {'album': album,'form': form,'error_message': 'You already added that song',
                })
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        print(file_type)
        if file_type not in AUDIO_FILE_TYPES:
            return render(request, 'music/add_song.html', {'album': album,'form': form,'error_message': 'Audio file must be WAV, MP3, or OGG',
            })

        song.save()
        return render(request, 'music/add_song.html', {'album': album,'form': form,'success_message': 'Successfull added!'})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/add_song.html', context)
    

class AlbumCreate(CreateView):
    model=Album
    fields=['album_title','artist','genre','album_logo']

    def get_success_url(self):
        return reverse('music-home')

class AlbumUpdate(UpdateView):
    model=Album
    fields=['album_title','artist','genre','album_logo']

    def get_success_url(self):
        return reverse('music-home')

class AlbumDelete(DeleteView):
    model=Album

    def get_success_url(self):
        return reverse('music-home')

def albumSongDelete(request,album_id,song_id):
    album=get_object_or_404(Album,pk=album_id)
    song=Song.objects.get(pk=song_id)
    song.delete()
    return redirect('/music/details/'+str(album_id)+'/')

def searchAlbumMatch(query,album):
    # print(album.album_title)
    if query.lower() in album.album_title.lower():
        return True

    if query.lower() in album.artist.lower():
        return True

    if query.lower() in album.genre.lower():
        return True
    return False

def searchSongAlbum(query,song):
    if query.lower() in song.song_title.lower():
        return True
    return False
    
def search(request):
    query=request.GET.get('search')
    searched_album=[]
    searched_song=[]
    all_albums=Album.objects.all()
    all_songs=Song.objects.all()
    for albums in all_albums:
        if searchAlbumMatch(query,albums):
            print(query,albums)
            searched_album.append(albums)
        
    for songs in all_songs:
        if searchSongAlbum(query,songs):
            searched_song.append(songs)


    return render(request,'music/search.html',{'all_album':searched_album,'all_songs':searched_song,'query':query})
