import folium
from folium.plugins import HeatMap
from get_earthquake_df import get_earthquake_df

# !!!Filter properties should be in frontend and sent by request.

# Create a popup content for each marker.
def create_popup_content(row):
    return f"""
        <h6>{row['Place']}</h6>
        <div style='display:flex;flex-direction:column;justify-content:space-between;'>
            <div><b>ML:</b> {row['ML']}</div>
            <div><b>Depth:</b> {row['Depth']}</div>
            <div><b>Datetime:</b> {row['Datetime']}</div>
        </div>
    """
# Create a marker for each row.
def create_marker(row):
    popup_content = create_popup_content(row)
    return folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_content,
        tooltip=row['Place'],
        icon=folium.Icon(color='red', icon='bolt',prefix="fa")
    )
# Create a heatmap from earthquake data.
def create_heatmap(_limit=50, _filter=None, _url='http://www.koeri.boun.edu.tr/scripts/lst2.asp'):
    #Get earthquake data.
    df = get_earthquake_df(filter=_filter, limit=_limit,url=_url)
    #Create a map object.
    map_obj = folium.Map(location=[39, 35], zoom_start=6)
    #Create a list of latitudes, longitudes and magnitudes. Magnitude is divided by 8 to make it more scalable. 
    #Otherwise, the heatmap would be too red. But this is not a good solution.
    lats_longs = [[row['Latitude'], row['Longitude'], row['ML'] / 8] for _, row in df.iterrows()]
    #Create a list of markers.
    markers = [create_marker(row) for _, row in df.iterrows()]
    #Add markers and heatmap to map object.
    for marker in markers:
        marker.add_to(map_obj)
    HeatMap(lats_longs).add_to(map_obj)
    #Save the map object as html. 
    return map_obj.get_root().render()