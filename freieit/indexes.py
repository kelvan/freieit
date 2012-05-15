import datetime
from haystack import indexes
from freieit.models import ExpertProfile


class ExpertProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #name = indexes.CharField(model_attr='name')
    #location = indexes.CharField(model_attr='location')
    #services = indexes.CharField(model_attr='services')

    def get_model(self):
        return ExpertProfile

    #def index_queryset(self):
        #"""Used when the entire index for model is updated."""
        #return self.get_model().objects.all()
