import netCDF4
from netCDF4 import Dataset
import os
import datetime
import csv

file_path = './enhanced_measurement.nc'
d = Dataset(file_path)
print(d.variables.keys())

lat=list(d.variables["lat_01"])
lon=list(d.variables["lon_01"])
lat20=list(d.variables["lat_20_ku"])
lon20=list(d.variables["lon_20_ku"])
time=list(d.variables["time_01"])
time20= list(d.variables["time_20_ku"])
alt20=list(d.variables["alt_20_ku"])
lat20=list(d.variables["lat_20_ku"])
lon20=list(d.variables["lon_20_ku"])
ice20=list(d.variables['range_ice_sheet_20_ku'])
iono20=list(d.variables['iono_cor_alt_20_ku'])
sea_surf20=list(d.variables["mean_sea_surf_sol1_20_ku"])
geoid=list(d.variables["geoid_01"])

model=list(d.variables["mod_dry_tropo_cor_zero_altitude_01"])
wet=list(d.variables["rad_wet_tropo_cor_01_ku"])
wetModel=list(d.variables["mod_wet_tropo_cor_meas_altitude_01"])

tide1=list(d.variables["solid_earth_tide_01"])
tide2=list(d.variables["pole_tide_01"])
iono_plrm=list(d.variables["iono_cor_alt_20_plrm_ku"])

index = 0

count=0
count2=0
with open('ps1_7.csv',mode='w') as file:

    file_writer=csv.writer(file,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
    file_writer.writerow(['Latitude','Longitude','Time','Value','alt_20_ku','range_ice_sheet_20_ku','iono_cor_alt_20_ku','mean_sea_surf_sol1_20_ku','geoid_01','mod_dry_tropo_cor_zero_altitude_01','rad_wet_tropo_cor_01_ku','mod_wet_tropo_cor_meas_altitude_01','solid_earth_tide_01','pole_tide_01'])

    for i in range(0,len(time)):
            index=0
            #For first 5 parameters The Latitude and Longitude dimensions are closest when the time dimension
            #for both the set of parameters are similar. By both set i mean smaller dimension and larger dimension 

            while index<len(time20) and abs(time[i]-time20[index])>0.04:
                index+=1

            if(index==len(time20)):
                continue
            lat_val = lat[i]
            lon_val = lon[i]

            time_val = time[i]

            lat20_val = lat20[index]
            lon20_val = lon20[index]

            time20_val = time20[index]
            alt_val = alt20[index]

            if(ice20[index]):
                ice_val = ice20[index]
            else:
                continue
            
            if(iono20[i]):
                iono_val = iono20[i]
            else:
                continue
            
            sea_surf_val = geoid[i]

            model_val = model[i]

            if(wet[i]):
                wet_val = wet[i]
            else:
                wet_val = wetModel[i]

            tide1_val = tide1[i]
            tide2_val = tide2[i]
            
            count+=1

            #ignore this part this is for date
            utctimestamp=datetime.datetime.timestamp(datetime.datetime(2000,1,1,0,0,0))
            date=datetime.date.fromtimestamp(time[i]+utctimestamp)

            #Calculation done here 
            ewl = alt_val - ice_val - iono_val - sea_surf_val
            ewr = model_val + wet_val + tide1_val + tide2_val

            print("Latitude : {} Longitude : {} time : {}".format(lat_val,lon_val,time_val))
            print("Latitude 20: {} Longitude 20: {} time 20: {}".format(lat20_val,lon20_val,time20_val))
            print("Value : {}".format(ewl-ewr))
            
            val=0
            if ewl!=ewr:
                val = ewl-ewr

            file_writer.writerow([lat_val,lon_val,time_val,val,alt_val,ice_val,iono_val,sea_surf_val,geoid[i],model_val,wet_val, wetModel[i], tide1_val,tide2_val])

            if(ewl-ewr>2):
                count2+=1
print("{} Enteries Displayed".format(count))
print("{} Enteries have Water Levels above 2m".format(count2))