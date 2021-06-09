from django.db import models
import cv2

# Create your models here.

class Album(models.Model):
    album_title=models.CharField(max_length=500)
    artist=models.CharField(max_length=200)
    genre=models.CharField(max_length=200) 
    album_logo=models.FileField()
    is_favorite=models.BooleanField(default=False)

    def __str__(self):
        return self.album_title+' - '+self.artist

    def save(self, *args, **kawrgs):
        super().save(*args,**kawrgs)

        img=cv2.imread(self.album_logo.path,1)
        img=cv2.resize(img,(3000,3000))
        cv2.imwrite(self.album_logo.path,img)

class Song(models.Model):
    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    song_title=models.CharField(max_length=250)
    audio_file=models.FileField(default='')
    is_favorite=models.BooleanField(default=False)

    def __str__(self):
        return self.song_title
