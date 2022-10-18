import sqlalchemy
import os
from .TPTI import df1
from .PGR1 import df2
from .GSI import df3
from .TSI import df4
from .BSI import df5
import pandas as pd
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

database_name = os.path.join(BASE_DIR, 'dbgempa.sqlite3')
database_url = 'sqlite:///{}'.format(database_name)
engine = sqlalchemy.create_engine(database_url, echo=False)

sql1 = "SELECT * FROM applatsar_databasegempa WHERE stasiun='BMKG-TPTI' ORDER By id DESC LIMIT 1;"
sql_df1 = pd.read_sql(sql=sql1, con=engine)

databaru1=df1['keterangan'].item()
datalama1=sql_df1['keterangan'].item()

def inputdata1():
  if databaru1!=datalama1:
    return df1.to_sql("applatsar_databasegempa", con=engine, if_exists="append", index=False)
  return False

sql2 = "SELECT * FROM applatsar_databasegempa WHERE stasiun = 'BMKG-PGR1' ORDER BY id DESC LIMIT 1;"
sql_df2 = pd.read_sql(sql=sql2, con=engine)

databaru2=df2['keterangan'].item()
datalama2=sql_df2['keterangan'].item()

def inputdata2():
  if databaru2!=datalama2:
    return df2.to_sql("applatsar_databasegempa", con=engine, if_exists="append", index=False)
  return False

sql3 = "SELECT * FROM applatsar_databasegempa WHERE stasiun = 'BMKG-GSI' ORDER BY id DESC LIMIT 1"
sql_df3 = pd.read_sql(sql=sql3, con=engine)

databaru3=df3['keterangan'].item()
datalama3=sql_df3['keterangan'].item()

def inputdata3():
  if databaru3!=datalama3:
    return df3.to_sql("applatsar_databasegempa", con=engine, if_exists="append", index=False)
  return False

sql4 = "SELECT * FROM applatsar_databasegempa WHERE stasiun = 'BMKG-TSI' ORDER BY id DESC LIMIT 1"
sql_df4 = pd.read_sql(sql=sql4, con=engine)

databaru4=df4['keterangan'].item()
datalama4=sql_df4['keterangan'].item()

def inputdata4():
  if databaru4!=datalama4:
    return df4.to_sql("applatsar_databasegempa", con=engine, if_exists="append", index=False)
  return False

sql5 = "SELECT * FROM applatsar_databasegempa WHERE stasiun = 'BMKG-BSI' ORDER BY id DESC LIMIT 1"
sql_df5 = pd.read_sql(sql=sql5, con=engine)

databaru5=df5['keterangan'].item()
datalama5=sql_df5['keterangan'].item()

def inputdata5():
  if databaru5!=datalama5:
    return df5.to_sql("applatsar_databasegempa", con=engine, if_exists="append", index=False)
  return False
