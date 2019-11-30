from django.db import models

from .validators import validate_lidwoord


class Lidwoord(models.Model):
    value = models.CharField(max_length=3, unique=True, validators=[validate_lidwoord])

    class Meta:
        verbose_name_plural = 'lidwoorden'

    def __str__(self):
        return self.value.capitalize()

class Woord(models.Model):
    lidwoord = models.ForeignKey(Lidwoord, on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=256)

    class Meta:
        verbose_name_plural = 'woorden'

    def __str__(self):
        return '({}) {}'.format(self.lidwoord.value.capitalize(), self.value)