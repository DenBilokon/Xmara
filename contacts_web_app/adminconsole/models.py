from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserFileSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pictures = models.IntegerField(default=0)
    videos = models.IntegerField(default=0)
    audio = models.IntegerField(default=0)
    documents = models.IntegerField(default=0)
    archives = models.IntegerField(default=0)
    summary_files = models.IntegerField(default=0)
    contacts = models.IntegerField(default=0)
    notes = models.IntegerField(default=0)

    def total_audio_files(self):
        return self.audio

    def total_picture_files(self):
        return self.pictures

    def total_video_files(self):
        return self.videos

    def total_document_files(self):
        return self.documents

    def total_archive_files(self):
        return self.archives

    def total_summary_files(self):
        return self.summary_files

    def total_contacts(self):
        return self.contacts

    def total_notes(self):
        return self.notes

