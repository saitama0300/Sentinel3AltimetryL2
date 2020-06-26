from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date

username = 'tanmay.29'
password = '123456789'
#You may change the username and password as per your need

api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

#Footprint is the region of interest for download 

n = read_geojson('.\\test2.geojson')
footprint = geojson_to_wkt(read_geojson('.\\test2.geojson'))

# in query args you may pass the date and time of start to end 
# for past 30 days keep it 'NOW-30DAYS','NOW'
'''A time interval filter based on the Sensing Start Time of the products. Expects a tuple of (start, end), e.g. (“NOW-1DAY”, “NOW”). The timestamps can be either a Python datetime or a string in one of the following formats:

        yyyyMMdd
        yyyy-MM-ddThh:mm:ss.SSSZ (ISO-8601)
        yyyy-MM-ddThh:mm:ssZ
        NOW
        NOW-<n>DAY(S) (or HOUR(S), MONTH(S), etc.)
        NOW+<n>DAY(S)
        yyyy-MM-ddThh:mm:ssZ-<n>DAY(S)
        NOW/DAY (or HOUR, MONTH etc.) - rounds the value to the given unit

'''

query_kwargs = {
        'platformname': 'Sentinel-3',
        'producttype': 'SR_2_LAN___',
        'date': ('NOW-30DAYS', 'NOW'),
        'timeliness':'Non-Time Critical'}

#For ingestion date keep it like [NOW-30DAYS] You will then download data within this ingestion date 
products = api.query(footprint,
                     **query_kwargs)

api.download_all(products)