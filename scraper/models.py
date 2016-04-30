from core.abstract_models import BaseModel, TitleAndSlugModel
from django.db import models


class Category(TitleAndSlugModel):
    ref = models.IntegerField()


class Trader(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField()
    category = models.ForeignKey(Category, related_name="traders")

    def __unicode__(self):
        return self.name
