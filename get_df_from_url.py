import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_html(_url):
    try:
        r = requests.get(_url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return requests.exceptions.RequestException

def get_pre(_html):
    soup = BeautifulSoup(_html, 'html.parser')
    pre = soup.find('pre')
    return pre

def get_rows(_pre):
    rows = _pre.text.split('\n')
    rows = rows[7:-2]
    return rows

def get_cols(_rows):
    cols = []
    for row in _rows:
        cols.append(row.split()[0:9])
    return cols

def create_df(_cols):
    df = pd.DataFrame(_cols, columns=['Date', 'Time', 'Latitude', 'Longitude', 'Depth', 'MD', 'ML', 'Mw', 'Place'])
    df.replace("-.-", None, inplace=True)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df.drop(['Date', 'Time'], axis=1, inplace=True)
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Latitude'] = pd.to_numeric(df['Latitude'])
    df['Longitude'] = pd.to_numeric(df['Longitude'])
    df['Depth'] = pd.to_numeric(df['Depth'])
    df['MD'] = pd.to_numeric(df['MD'])
    df['ML'] = pd.to_numeric(df['ML'])
    df['Mw'] = pd.to_numeric(df['Mw'])
    df['Place'] = df['Place'].str.strip()
    df = df[['Datetime', 'Latitude', 'Longitude', 'Depth', 'MD', 'ML', 'Mw', 'Place']]
    return df
    
def main():
    url = 'http://www.koeri.boun.edu.tr/scripts/lst2.asp'
    limit = 500
    html = get_html(url)
    pre = get_pre(html)
    rows = get_rows(pre)
    cols = get_cols(rows)
    df =create_df(cols)

if __name__ == '__main__':
    main()