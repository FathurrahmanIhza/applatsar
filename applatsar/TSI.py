import pandas as pd
from bs4 import BeautifulSoup
import haversine as hs
import math
import pandas as pd
import requests
from django.conf import settings
import sqlalchemy
import os

url = "http://202.90.198.127/esdxsta/log/tuntungan.php"
data = requests.get(url).text
soup = BeautifulSoup(data, 'html.parser')

# Creating list with all tables
table = soup.find('pre')
stasiun = "BMKG-TSI"
gempa = table.text
f = open("gempa.txt", "w")
f.write(gempa)
f.close()

fileinput = 'gempa.txt'
fileoutput = 'gempa.pha'

# baca isi file input dan buka file output
file = open(fileinput,'r')
baris = file.readlines()
for i in range(len(baris)):
	baris[i]=baris[i].split()
file.close()
file = open(fileoutput,'w')

# catat tiap baris file input ke file output
i = 0
while i < len(baris):
    if len(baris[i]) > 0 and baris[i][0] == 'Origin:':
        tahun = (('%2d') % float(baris[i + 1][1].split('-')[0]))
        thn = int(tahun)
        bulan = baris[i + 1][1].split('-')[1].zfill(1)
        bln = int(bulan)
        tanggal = baris[i + 1][1].split('-')[2].zfill(1)
        tgl = int(tanggal)
        jam = baris[i + 2][1].split(':')[0].zfill(2)
        menit = baris[i + 2][1].split(':')[1].zfill(2)
        detik = (('%.2f') % float(baris[i + 2][1].split(':')[2])).zfill(4)
        lintang = (float(baris[i + 3][1]))
        if float(lintang) > 0:
            NS = "N"
        else:
            NS = "S"
        bujur = (float(baris[i + 4][1]))
        depth = (int(baris[i + 5][1]))
        #mag2 = ('%.1f') % float(baris[i + 14][1])
        for j in range(0, 100):
            #print(baris[i + 13 + j])
            if baris[i + 13 + j][-1] == 'preferred':
                mag = ('%.1f') % float(baris[i + 13 + j][1])
                break
        #print(mag)
        rms = ('%.3f') % float(baris[i + 9][2])
        time0 = float(detik) + float(menit) * 60 + float(jam) * 60 * 60
    i = i + 1

file.close()

# input total detik
totaldetik = int(time0) + 25200

if totaldetik > 86400:
    totaldetik=totaldetik-86400
    tgl=tgl+1

if tgl > 31:
    tgl=tgl-31
    bln=bln+1

if bln > 12:
    bln=bln-12
    thn=thn+1

# melakukan konversi hh:mm:ss ke detik
hh = totaldetik // 3600
sisadetik = totaldetik % 3600
mm = sisadetik // 60
ss = sisadetik % 60

# menampilkan hasil konversi

time = "%02d:%02d:%02d" %(hh,mm,ss)
waktu = "%02d-%02d-%02d" %(thn, bln, tgl)

Epic=(lintang, bujur)
Medan=(3.35, 98.40)
Binjai=(3.60, 98.48)
Siantar=(2.96, 99.06)
Sibolga=(1.74, 98.77)
Brastagi=(3.19, 98.48)
Nias=(1.03, 97.76)
Balige=(2.18, 99.06)
PadangLawasUtara=(1.46, 99.67)
PadangSidempuan=(1.36, 99.26)
TapanuliUtara=(2.00, 99.07)
TapanuliSelatan=(1.51, 99.25)
Subulussalam=(2.64, 98.00)
Tapaktuan=(3.15, 97.10)
Meulaboh=(4.45, 96.18)
Simeulue=(2.61, 96.08)
BlangPidie=(3.79, 95.91)
Calang=(4.38, 95.35)
BandaAceh=(5.55, 95.31)
Jantho=(5.37, 95.53)
Sabang=(5.89, 95.32)
Pidie=(5.08, 96.11)
PidieJaya=(5.15, 96.21)
Kutacane=(3.37, 97.68)
Singkil=(2.33, 97.67)
Takengon=(4.33, 96.33)
GayoLues=(4.00, 97.00)
Langsa=(4.47, 97.95)
Lhokseumawe=(5.18, 97.15)
Bireuen=(5.08, 96.60)
BenerMeriah=(4.75, 97.00)

kota = [Medan, Binjai, Siantar,
        Sibolga, Brastagi, Nias, Balige,
        PadangLawasUtara, PadangSidempuan, 
        TapanuliUtara, TapanuliSelatan, Subulussalam,
        Tapaktuan, Meulaboh, Simeulue,
        BlangPidie, Calang, BandaAceh,
        Jantho, Sabang, Pidie, PidieJaya,
        Kutacane, Singkil, Takengon, GayoLues,
        Langsa, Lhokseumawe, Bireuen, BenerMeriah]

namakota = ["Medan", "Binjai", "Siantar",
            "Sibolga", "Brastagi", "Nias", "Balige",
            "Padang Lawas Utara", "Padang Sidempuan", 
            "Tapanuli Utara", "Tapanuli Selatan", "Subulussalam",
            "Tapaktuan", "Meulaboh", "Simeulue",
            "Blang Pidie", "Calang", "Banda Aceh",
            "Jantho", "Sabang", "Pidie", "Pidie Jaya",
            "Kutacane", "Singkil", "Takengon", "Gayo Lues",
            "Langsa", "Lhokseumawe", "Bireuen", "Bener Meriah"]
            
def direction_lookup(origin_x, origin_y, destination_x, destination_y):
    deltaX = origin_x - destination_x 
    deltaY = origin_y - destination_y 
    degrees_temp = math.atan2(deltaX, deltaY)/math.pi*180
    
    if degrees_temp < 0:
        degrees_final = 360 + degrees_temp
    else:
        degrees_final = degrees_temp

    compass_brackets = ["Utara", "Timur Laut", "Timur", "Tenggara", "Selatan", "Barat Daya", "Barat", "Barat Laut", "Utara"]
    compass_lookup = round(degrees_final / 45)
    return compass_brackets[compass_lookup]

keterangankota = {}

i = 0
while i < len(namakota):
    jarak = int((hs.haversine(Epic, kota[i])))
    arah = direction_lookup(Epic[0], Epic[1], kota[i][0], kota[i][1])
    keterangankota[jarak] = "%d km %s %s" % (jarak, arah, namakota[i])
    i = i + 1
ketkota = []
for k, v in sorted(keterangankota.items()):
    ketkota.append(v)

keterangan = ketkota[0]


# initialize list of lists
data = [[stasiun, waktu, time, lintang, bujur, depth, mag, keterangan]]
  
df4 = pd.DataFrame(data, columns=['stasiun', 'tanggal', 'jam','lintang','bujur','kedalaman','magnitudo', 'keterangan'])

