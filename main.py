import pandas as pd
import requests
import wget
import folium
from folium.plugins import MarkerCluster

# filename = wget.download("http://www.edinburgh.gov.uk/download/downloads/id/11854/tables_and_chairs_permits.csv")
filename = "Tables_and_Chairs_Live_Permits.csv"
df0 = pd.read_csv(filename, encoding="ISO-8859-1")
df0.head()

# dropping duplicate entries
df1 = df0.loc[:, ['Premises Name', 'Premises Address']]
df1 = df1.drop_duplicates()

# in 2012: 280
print(df1.shape[0])


def query_address(address):
    """Return response from open streetmap.

    Parameter:
    address - address of establishment

    Returns:
    result - json, response from open street map
    """

    url = "https://nominatim.openstreetmap.org/search"
    parameters = {'q':'{}, Edinburgh'.format(address), 'format': 'json'}

    response = requests.get(url, params=parameters)
    # don't want to raise an error to not stop the processing
    # print address instead for future inspection
    if response.status_code != 200:
        print("Error querying {}".format(address))
        result = {}
    else:
        result = response.json()
    return result


df1['json'] = df1['Premises Address'].map(lambda  x: query_address(x))

# drop empty responses
df2 = df1[df1['json'].map(lambda d: len(d)) > 0].copy()
print(df2.shape[0])
