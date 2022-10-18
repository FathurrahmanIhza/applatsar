from django.shortcuts import redirect, render
import urllib.request, json
from django.http import HttpResponse
from django.template import loader
from applatsar.models import Databasegempa
from applatsar.models import DatabaseTamu
from applatsar.filters import GempaFilter, TamuFilter
from applatsar.forms import FormTamu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .printDB import *
import folium
from folium.plugins import MiniMap
from django.contrib.auth.decorators import login_required
from django.conf import settings

inputdata1()
inputdata2()
inputdata3()
inputdata4()
inputdata5()

def index(request):
    with urllib.request.urlopen("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json") as url2:
        data2 = json.loads(url2.read().decode())

    index = loader.get_template('index.html')
    context = {
        'gempadirasakan': data2['Infogempa']['gempa'],
    }
    return render(request, 'index.html', context)

def sejarah(request):
    return render(request, 'sejarah.html')

def gempadirasakan(request):
    return render(request, 'gempadirasakan.html')

def gempaterkini(request):
    return render(request, 'gempaterkini.html')

def login(request):
    return render(request, 'login.html')

def visimisi(request):
    return render(request, 'visi&misi.html')

def pegawai(request):
    return render(request, 'pegawai.html')

def gempadirasakan(request):
    with urllib.request.urlopen("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json") as url1:
        data1 = json.loads(url1.read().decode())

    tmpdaftargempa = loader.get_template('gempadirasakan.html')
    context = {
        'gempa': data1['Infogempa']['gempa'],
    }
    return HttpResponse(tmpdaftargempa.render(context, request)) 

url_base = 'http://server.arcgisonline.com/ArcGIS/rest/services/'
service = 'NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}'
tileset = url_base + service
    
@login_required(login_url=settings.LOGIN_URL) 
def sigempa(request):
    g = GempaFilter(request.GET, queryset=Databasegempa.objects.order_by('-tanggal','-jam'))
    paginator = Paginator(g.qs, 8)
    page_number = request.GET.get('page', 1)
    try:
        response = paginator.page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        response = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        response = paginator.page(paginator.num_pages)

    for item in response:
        m = folium.Map([item.lintang, item.bujur], zoom_start=6.5, tiles=tileset, attr='USGS style')
        test = folium.Html(item.keterangan, script=True)
        popup = folium.Popup(test, max_width=2650)
        folium.Circle(location=[item.lintang, item.bujur], 
                        popup=popup, 
                        fill=True,
                        radius=10000, 
                        fill_color="red",        
                        opacity=0.1,
                        fill_opacity=1,
                        color="red").add_to(m)
        minimap = MiniMap(position="bottomleft",zoom_level_offset=-4, width=100, height=60)
        m.add_child(minimap)
        m=m._repr_html_() #updated
        item.map=m
    context = {
        'myFilter' : g,
        'DataGempa' : response,
    }
    return render(request, 'sigempa.html', context)

@login_required(login_url=settings.LOGIN_URL) 
def gambar(request, id):
    item = Databasegempa.objects.get(pk=id)

    m = folium.Map([item.lintang, item.bujur], zoom_start=6.5, tiles=tileset, attr='USGS style', useCORS='true')
    test = folium.Html(item.keterangan, script=True)
    popup = folium.Popup(test, max_width=2650)
    folium.Circle(location=[item.lintang, item.bujur], 
                    popup=popup, 
                    fill=True,
                    radius=10000, 
                    fill_color="red",        
                    opacity=0.1,
                    fill_opacity=1,
                    color="red").add_to(m)
    minimap = MiniMap(position="bottomleft",zoom_level_offset=-4, width=100, height=60)
    m.add_child(minimap)
    m=m._repr_html_() #updated
    item.map=m

    context = {
        'item' : item,
    }
    return render(request, 'gambar.html', context)

@login_required(login_url=settings.LOGIN_URL) 
def sitamu(request):
    if request.method == "POST":
        form = FormTamu(request.POST)
        if form.is_valid():
            form.save()
            form = FormTamu()
            pesan = "Data Berhasil Disimpan!"
            context ={
                'formtamu' : form,   
                'pesan' : pesan, 
            }
            return redirect('/sitamu/', context)
    else:
        form = FormTamu()

    context ={
        'formtamu' : form,
    }
    return render(request, 'sitamu.html', context)

def siritamu(request):
    t = TamuFilter(request.GET, queryset=DatabaseTamu.objects.order_by('-tanggal','-jam'))
    paginator = Paginator(t.qs, 12)
    page_number = request.GET.get('page', 1)
    try:
        response = paginator.page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        response = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        response = paginator.page(paginator.num_pages)
    context = {
        'myFilter' : t,
        'DataTamu' : response,
    }
    return render(request, 'siritamu.html', context)


datasensor = {'kode': ["MLSI","BESM","SNSI","TPTI","KUSI","KLSM","SSSI","KCSI","SDSM","SPSM"],
        'tipe' : ["Libra (Ina)", "MiniReg (Ina)", "Libra (Ina)", "CEA (China)", "Type A", "MiniReg (Ina)", "REIS (Jepang)",
                  "Libra (Ina)", "MiniReg (Ina)","MiniReg (Ina)"],
        'daerah': ["Beutong, Aceh Barat", "Nagan Raya, Aceh Barat", "Sinabang, Simeulue", "Tapaktuan, Aceh Selatan",
                   "Kluet Tengah, Aceh Selatan", "Kluet Utara, Aceh Selatan", "Subulussalam", "Kutacane, Aceh Tenggara",
                   "Sidikalang, Dairi", "STTU, Pakpak Bharat"],
        'lati' : [4.26, 4.15, 2.40, 3.26, 3.19, 3.08, 2.67, 3.52, 2.51, 2.75],
        'long' : [96.40, 96.32, 96.32, 96.17, 96.37, 96.32, 96.97, 96.77, 96.37, 96.28]}

dfs = pd.DataFrame(datasensor)

@login_required(login_url=settings.LOGIN_URL) 
def sisensor(request):
    mp = folium.Map([3.25, 97.0], zoom_start=8)
    tooltip = "Cek Sensor"
    """for lati,long,kode,tipe,daerah in zip(dfs['lat'],dfs['long'],dfs['kode'],dfs['daerah']):    

    folium.Marker(location=[lati, long],popup = popup1, tooltip=tooltip).add_to(mp)"""
    folium.Marker(
    [3.17, 97.28], popup="Stasiun Geofisika Aceh Selatan", icon=folium.Icon(color='#8000ff',icon_color='#4df3ce', icon="star", prefix="fa")).add_to(mp)
    folium.Marker(
    [4.26, 96.40], popup="MLSI - LIBRA (Ina) - Beutong, Aceh Barat", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [4.15, 96.32], popup="BESM - MiniReg (Ina) - Nagan Raya, Aceh Barat", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [2.40, 96.32], popup="SNSI - LIBRA (Ina) - Sinabang, Simeulue", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [3.26, 97.17], popup="TPTI - CEA (China) - Tapaktuan, Aceh Selatan", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [3.19, 97.37], popup="KUSI - Type A - Kluet Tengah, Aceh Selatan", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [3.08, 97.32], popup="KLSM - MiniReg (Ina) - Kluet Utara, Aceh Selatan", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [2.67, 97.97], popup="SSSI - REIS (Jepang) - Subulussalam", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [3.52, 97.77], popup="KCSI - LIBRA (Ina) - Kutacane, Aceh Tenggara", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [2.51, 98.37], popup="SPSM - MiniReg (Ina) - STTU, Pakpak Bharat", tooltip=tooltip).add_to(mp)
    folium.Marker(
    [2.75, 98.28], popup="SDSM - MiniReg (Ina) - Sidikalang, Dairi", tooltip=tooltip).add_to(mp)
    

    minimap = MiniMap(position="bottomleft",zoom_level_offset=-4, width=150, height=100)
    mp.add_child(minimap)
    mp=mp._repr_html_() #updated
    item=mp

    context = {
        'item' : item,
    }
    return render(request, 'sisensor.html', context)
