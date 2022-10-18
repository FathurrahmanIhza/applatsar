from django.db import models


STASIUN_CHOICES = (
    ("BMKG-PGR1","BMKG-PGR1"),
    ("BMKG-TPTI","BMKG-TPTI"),
    ("BMKG-TSI","BMKG-TSI"),
    ("BMKG-GSI","BMKG-GSI"),
    ("BMKG-BSI","BMKG-BSI"),   
)

class Databasegempa(models.Model):
    stasiun = models.CharField(max_length=20, null=True, choices = STASIUN_CHOICES, default = '2')
    tanggal = models.DateField(null=True)
    jam = models.IntegerField(null=True)
    lintang = models.FloatField(null=True)
    bujur = models.FloatField(null=True)
    kedalaman = models.IntegerField(null=True)
    magnitudo = models.DecimalField(decimal_places=1, max_digits=4, null=True)
    keterangan = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.keterangan

class DatabaseTamu(models.Model):
    nama = models.CharField(max_length=30, null=True)
    tanggal = models.DateField(null=True, auto_now_add = True)
    jam = models.TimeField(null=True, auto_now_add = True)
    instansi = models.CharField(max_length=30, null=True)
    agenda = models.TextField(null=True)

    def __str__(self):
        return self.nama

