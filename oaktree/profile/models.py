from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver
import re, unicodedata
from oaktree.core.abstract_models import BaseModel


class UserProfile(BaseModel):
	"""
	Profile and configurations for a user
	"""
	user = OneToOneField(User, related_name="profile", editable=False)

	def get_absolute_url(self):
		return reverse('profile', args=[self.user.username])

	@property
	def username(self):
		return self.user.username

	@property
	def first_name(self):
		return self.user.first_name

	@property
	def last_name(self):
		return self.user.last_name

	def __unicode__(self):
		user = self.user
		if user.first_name:
			return "%s %s" % (user.first_name, user.last_name)
		else:
			return user.username
