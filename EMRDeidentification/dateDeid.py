import datetime as dt 
import numpy as np
import pandas as pd 

date1 = dt.datetime.strptime('08-11-2022', '%d-%m-%Y')
date2 = dt.datetime.strptime('10-11-2022', '%d-%m-%Y')

dt1_utc = date1.replace(tzinfo=dt.timezone.utc)
dt2_utc = date2.replace(tzinfo=dt.timezone.utc)

print(dt1_utc)
print(dt2_utc)

print((dt2_utc - dt1_utc).days)

#Convert to unix timestamp
dt1_unix = dt1_utc.timestamp()
dt2_unix = dt2_utc.timestamp()

print(dt1_unix)
print(dt2_unix)

#Drop the first digit and replace with zero
dt1_unix_deid = float('0' + str(dt1_unix)[1:])
dt2_unix_deid = float('0' + str(dt2_unix)[1:])

print(dt1_unix_deid)
print(dt2_unix_deid)

#Unix timestamp to date
dt1_deid = dt.datetime.utcfromtimestamp(dt1_unix_deid)
dt2_deid = dt.datetime.utcfromtimestamp(dt2_unix_deid)

print(dt1_deid)
print(dt2_deid)
