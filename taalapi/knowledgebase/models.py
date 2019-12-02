from django.db import models

from .validators import validate_lidwoord


class Lidwoord(models.Model):
    lidwoord = models.CharField(max_length=3, unique=True, validators=[validate_lidwoord])

    class Meta:
        verbose_name_plural = 'lidwoorden'

    def __str__(self):
        return self.lidwoord

class Woord(models.Model):
    lidwoord = models.ForeignKey(Lidwoord, on_delete=models.DO_NOTHING)
    woord = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'woorden'

    def __str__(self):
        return '({}) {}'.format(self.lidwoord.lidwoord, self.woord)
