from django.core.validators import ValidationError


def validate_lidwoord(value):
    """
    In Dutch language, there are only two lidwoorden: "de" and "het".
    """

    if value.lower() not in ['de', 'het']:
        raise ValidationError("{} is not a correct lidwoord.".format(value))
