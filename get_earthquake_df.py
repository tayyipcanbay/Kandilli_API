import requests
from bs4 import BeautifulSoup
import pandas as pd

default_url = 'http://www.koeri.boun.edu.tr/scripts/lst2.asp'
default_limit = 500
default_filter = {
    "Datetime": {'ASC': True},
    "Magnitude": {"min": 0, "max": 10},
}

def get_html(_url):
    #Gets html from url
    try:
        r = requests.get(_url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return requests.exceptions.RequestException

def get_pre(_html):
    #Gets the first pre tag in HTML. Because the data is in the first pre tag.
    soup = BeautifulSoup(_html, 'html.parser')
    pre = soup.find('pre')
    return pre

def get_rows(_pre):
    #For each row in pre tag, splits the row by new line and returns the rows.
    rows = _pre.text.split('\n')
    #First 7 rows are not data. Last 2 rows are not data.
    rows = rows[7:-2]
    return rows

def get_cols(_rows):
    #For each row in rows, splits the row by space and returns the columns.
    cols = []
    for row in _rows:
        #We only need the first 9 columns.
        cols.append(row.split()[0:9])
    return cols

def filter_df(_df, _filter):
    #Filters the dataframe by _filter.
    #_filter is a dictionary.
    #_filter = {
    #    "Datetime": {'ASC': True},
    #    "Magnitude": {min: 0, max: 10},
    #}
    #If _filter is not specified, returns the dataframe without filtering.
    if _filter is None:
        return _df
    #Filter by Datetime
    if "Datetime" in _filter:
        _df = _df.sort_values(by=['Datetime'], ascending=_filter['Datetime']['ASC'])
    #Filter by Magnitude
    if "Magnitude" in _filter:
        _df = _df[(_df['ML'] >= _filter['Magnitude']['min']) & (_df['ML'] <= _filter['Magnitude']['max'])]
    return _df

def create_df(_cols, _filter):
    #Creates a dataframe from columns.
    df = pd.DataFrame(_cols, columns=['Date', 'Time', 'Latitude', 'Longitude', 'Depth', 'MD', 'ML', 'Mw', 'Place'])
    #Replace -.- with None
    df.replace("-.-", None, inplace=True)
    #Create a single Datetime column instead of Date and Time columns.
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df.drop(['Date', 'Time'], axis=1, inplace=True)
    #Convert columns to types.
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    df['Depth'] = pd.to_numeric(df['Depth'])
    df['MD'] = pd.to_numeric(df['MD'])
    df['ML'] = pd.to_numeric(df['ML'])
    df['Mw'] = pd.to_numeric(df['Mw'])
    df['Place'] = df['Place'].str.strip()
    #Reorder columns for better readability.
    df = df[['Datetime', 'Latitude', 'Longitude', 'Depth', 'MD', 'ML', 'Mw', 'Place']]
    #Filter the dataframe
    df = filter_df(df, _filter)
    return df
    
def get_earthquake_df(filter=default_filter,limit=default_limit,url=default_url):
    #Gets the dataframe from url and returns the dataframe.
    #If limit is not specified, returns the first 500 rows.
    #If url is not specified, returns the first 500 rows from http://www.koeri.boun.edu.tr/scripts/lst2.asp
    html = get_html(url)
    pre = get_pre(html)
    rows = get_rows(pre)
    cols = get_cols(rows)
    df =create_df(cols,filter)
    return df.head(limit)
