from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField


class Challenge_User(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(default="please add some content here")
    added_username = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=255,
    )

    def __unicode__(self):
        return str(self.name)


class Challenge(models.Model):
    status_choices = (
        ("Finished", "Finished"),
        ("Uncomplete", "Uncomplete")
    )
    author = models.ForeignKey(User)
    title = models.CharField(
        unique=True,
        max_length=255,
        help_text="""the name of the title""")
    slug = AutoSlugField(
        populate_from='title',
        unique=True)
    content = models.TextField(
        blank=False,
        default="please add some content here",
        help_text="""The contents of the article in Markdown.""")
    category = models.ForeignKey(Category)
    status = models.CharField(
        max_length=32,
        choices=status_choices,
        default="Uncomplete")
    date_modified = models.DateTimeField(
        auto_now=True)
    date_created = models.DateTimeField(
        auto_now_add=True)

    def vote_count(self):
        total = Vote.objects.filter(challenge=self).aggregate(models.Sum('direction'))
        if total['direction__sum'] is None:
            return 0
        else:
            return total['direction__sum']

    def __unicode__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('challenge_details', kwargs={'pk': self.id})


class Claim(models.Model):
    class Meta:
        unique_together = ("challenge", "author")

    status_choices = (
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Pending", "Pending")
    )
    challenge = models.ForeignKey(Challenge)
    author = models.ForeignKey(User)
    content = models.TextField(
        default="please add some content here",
        help_text="""Tell us about your claim""")
    project_url = models.URLField(
        blank=True
    )
    proof_url = models.URLField(
        blank=False
    )
    status = models.CharField(
        max_length=32,
        choices=status_choices,
        default="Pending")
    date_created = models.DateTimeField(
        auto_now_add=True)

    def __unicode__(self):
        return str(self.challenge) + " by " + str(self.author)

    def get_absolute_url(self):
        return reverse('claim_details', kwargs={'pk': self.id})


class Vote(models.Model):
    class Meta:
        unique_together = ("challenge", "user")

    user = models.ForeignKey(User)
    challenge = models.ForeignKey(Challenge)
    direction = models.IntegerField(default=0)
    date_created = models.DateTimeField(
        auto_now_add=True)

    def __unicode__(self):
        return str(self.user) + "->" + str(self.challenge) + ":" + str(self.direction)


class Award(models.Model):
    title = models.CharField(
        unique=True,
        max_length=255,
        help_text="""the name of the title""")
    about = models.TextField(
        default="please add some content here",
        help_text="""The contents of the article in Markdown.""")
    icon = models.CharField(max_length=255)

    def __unicode__(self):
        return str(self.title)