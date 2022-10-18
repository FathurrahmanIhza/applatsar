import django_filters
from .models import Databasegempa, DatabaseTamu, STASIUN_CHOICES
from django_filters import CharFilter
from django_filters import ChoiceFilter
from django import forms


class GempaFilter(django_filters.FilterSet):
    stasiun = ChoiceFilter(choices=STASIUN_CHOICES, widget=forms.Select
                            (attrs={'class': 'w3-round w3-border-0 marginform'}))
    Keterangan = CharFilter(field_name="keterangan", lookup_expr='icontains', label="Lokasi",
                            widget=forms.TextInput(attrs={'class': 'w3-round w3-border-0 marginform'}))

    class Meta:
        model = Databasegempa
        fields = ['stasiun','Keterangan']

class TamuFilter(django_filters.FilterSet):
    nama = CharFilter(field_name="nama", lookup_expr='icontains', label="Nama",
                            widget=forms.TextInput(attrs={'class': 'w3-round w3-border-0 marginform'}))
    instansi = CharFilter(field_name="instansi", lookup_expr='icontains', label="Instansi",
                            widget=forms.TextInput(attrs={'class': 'w3-round w3-border-0 marginform'}))

    class Meta:
        model = DatabaseTamu
        fields = ['nama','instansi']