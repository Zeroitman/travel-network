from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from rest_framework import status
from rest_framework.decorators import api_view
from social_network.models import Country, Post
from social_network.serializers.country import CountrySerializer
from source.constants import API_SECURE_KEY
from source.utils import MediaResponse


class CountryListView(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'country/country_list.html'

    def get_queryset(self):
        list_country = [str(a.post_country) for a in Post.objects.all()]
        return Country.objects.filter(name__in=list_country)


class CountryDetailView(LoginRequiredMixin, DetailView):
    model = Country
    template_name = 'country/country_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now_pk = int(self.kwargs.get('pk'))
        post_list = Post.objects.filter(post_country=now_pk).order_by('-created_date')
        context['post_list'] = post_list
        return context


@api_view(['GET'])
def countries(request):
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    list_country = [str(a.post_country) for a in Post.objects.all()]
    serializer = CountrySerializer(Country.objects.filter(name__in=list_country), many=True)
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("FAIL", details="NO_DATA", code=status.HTTP_200_OK, result=[])


@api_view(['GET'])
def country(request, pk):
    if request.headers.get('API-SECURE-KEY') != API_SECURE_KEY:
        return MediaResponse("FAIL", "INVALID_SECURE_KEY", code=status.HTTP_400_BAD_REQUEST)
    serializer = CountrySerializer(Country.objects.filter(pk=pk).first())
    if serializer.data:
        return MediaResponse("SUCCESS", "", code=status.HTTP_200_OK, result=serializer.data)
    return MediaResponse("FAIL", details="NO_DATA", code=status.HTTP_200_OK, result=[])
