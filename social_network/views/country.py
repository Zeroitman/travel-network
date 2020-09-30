from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from social_network.models import Country, Post


class CountryListView(ListView, LoginRequiredMixin):
    model = Country
    template_name = 'country/country_list.html'

    def get_queryset(self):
        list_country = []
        for a in Post.objects.all():
            list_country.append(str(a.post_country))
        return Country.objects.filter(name__in=list_country)


class CountryDetailView(DetailView, LoginRequiredMixin):
    model = Country
    template_name = 'country/country_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_pk = int(self.kwargs.get('pk'))
        post_list = Post.objects.filter(post_country=now_pk).order_by('-created_date')
        context['post_list'] = post_list
        return context
