
from django.db import models
from oaktree.core.abstract_models import TitleAndSlugModel, BaseModel


class Category(TitleAndSlugModel):
    ref = models.IntegerField(default=20)


class Trader(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    url = models.URLField()
    category = models.ForeignKey(Category, related_name="traders", blank=True, null=True)

    def __unicode__(self):
        return self.name
