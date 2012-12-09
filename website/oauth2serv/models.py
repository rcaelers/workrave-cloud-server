from django.db import models
from django.contrib.auth.models import User

from .settings import SCOPE_LENGTH
from .settings import CLIENT_ID_LENGTH, CLIENT_SECRET_LENGTH
from .settings import CODE_LENGTH, CODE_LIFETIME
from .settings import ACCESS_TOKEN_LENGTH, ACCESS_TOKEN_LIFETIME
from .settings import REFRESH_TOKEN_LENGTH

from utils import generate_key, generate_timestamp

TAGLINE_LENGTH = 250

class Scope(models.Model):
    name = models.CharField(
        "Scope name",
        help_text='Scope identifier.',
        max_length=SCOPE_LENGTH,
        unique=True)

    title = models.CharField(
        "Scope title",
        help_text='Human-friendly name of the scope.',
        max_length=SCOPE_LENGTH,
        unique=True)

    description = models.TextField(
        "Scope description",
        help_text='Extended description of scope purpose.',
        blank=True
    )

    parent = models.ForeignKey(
        'self',
        verbose_name='Parent scope',
        help_text='.',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Scope'
        verbose_name_plural = 'Scopes'
        ordering = ['name']

    def __unicode__(self):
        return '%s' % self.name


class Client(models.Model):
    PROFILE_NATIVE = 1
    PROFILE_WEB = 2

    PROFILE_CHOICES = (
        (PROFILE_NATIVE, 'Native application'),
        (PROFILE_WEB, 'Web application'),
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    profile = models.IntegerField(
        choices=PROFILE_CHOICES,
        default = PROFILE_WEB
    )

    user = models.ForeignKey(
        User,
        blank=True,
        null=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True
    )

    client_id = models.CharField(
        max_length=CLIENT_ID_LENGTH,
        default=generate_key(CLIENT_ID_LENGTH)
    )

    client_secret = models.CharField(
        max_length=CLIENT_SECRET_LENGTH,
        default=generate_key(CLIENT_SECRET_LENGTH)
    )

    redirect_uri = models.URLField()

    scopes = models.ManyToManyField(
        Scope,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __unicode__(self):
        return '%s' % self.name


class CodeGrant(models.Model):
    user = models.ForeignKey(
        User
    )

    client = models.ForeignKey(
        Client
    )

    code = models.CharField(
        max_length=CODE_LENGTH,
        default=generate_key(CODE_LENGTH),
        unique=True,
        db_index=True
    )

    description = models.TextField(
        blank=True
    )

    tagline = models.CharField(
        max_length=TAGLINE_LENGTH,
        blank=True
    )

    redirect_uri = models.URLField()

    scopes = models.ManyToManyField(
        Scope,
        blank=True,
        null=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True
    )

    expires = models.DateTimeField(
        default=generate_timestamp(CODE_LIFETIME)
    )

    class Meta:
        verbose_name = 'Code grant'
        verbose_name_plural = 'Code grants'

    def __unicode__(self):
        return '%s' % self.code


class Token(models.Model):
    user = models.ForeignKey(
        User
    )

    client = models.ForeignKey(
        Client
    )

    code = models.CharField(
        max_length=CODE_LENGTH,
        default=generate_key(CODE_LENGTH),
        unique=True,
        db_index=True
    )

    access_token = models.CharField(
        max_length=ACCESS_TOKEN_LENGTH,
        default=generate_key(ACCESS_TOKEN_LENGTH),
        unique=True,
        db_index=True
    )

    refresh_token = models.CharField(
        max_length=REFRESH_TOKEN_LENGTH,
        default=generate_key(REFRESH_TOKEN_LENGTH),
        unique=True,
        db_index=True,
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    tagline = models.CharField(
        max_length=TAGLINE_LENGTH,
        blank=True
    )

    scopes = models.ManyToManyField(
        Scope,
        blank=True,
        null=True
    )

    create_date = models.DateTimeField(
        auto_now_add=True
    )

    expires = models.DateTimeField(
        default=generate_timestamp(ACCESS_TOKEN_LIFETIME)
    )

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def __unicode__(self):
        return '%s' % self.code
