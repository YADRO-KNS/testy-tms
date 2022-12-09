from django.db import models


class TestrailSettings(models.Model):
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    api_url = models.CharField(max_length=255)
    dumpfile_path = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.login


class TestrailBackup(models.Model):
    name = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name
