from django.db import models

from .validators import validate_lidwoord


class Lidwoord(models.Model):
    lidwoord = models.CharField(max_length=3, unique=True, validators=[validate_lidwoord])

    class Meta:
        verbose_name_plural = 'lidwoorden'

    def __str__(self):
        return self.lidwoord

class Woord(models.Model):
    lidwoord = models.ManyToManyField(Lidwoord)
    woord = models.CharField(max_length=256)
    accurate = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'woorden'

    def __str__(self):
        return '({}) {}'.format('/'.join(self.lidwoord.values_list('lidwoord', flat=True)), self.woord)
