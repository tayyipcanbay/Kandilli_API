import folium
from folium.plugins import HeatMap
from get_earthquake_df import get_earthquake_df

def create_popup_content(row):
    return f"""
        <h6>{row['Place']}</h6>
        <div style='display:flex;flex-direction:column;justify-content:space-between;'>
            <div><b>ML:</b> {row['ML']}</div>
            <div><b>Depth:</b> {row['Depth']}</div>
            <div><b>Datetime:</b> {row['Datetime']}</div>
        </div>
    """

def create_marker(row):
    popup_content = create_popup_content(row)
    return folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_content,
        tooltip=row['Place'],
        icon=folium.Icon(color='red', icon='bolt',prefix="fa")
    )

def create_heatmap(limit=50):
    df = get_earthquake_df(limit)
    map_obj = folium.Map(location=[39, 35], zoom_start=6)
    
    lats_longs = [[row['Latitude'], row['Longitude'], row['ML'] / 8] for _, row in df.iterrows()]
    
    markers = [create_marker(row) for _, row in df.iterrows()]
    
    for marker in markers:
        marker.add_to(map_obj)
    
    HeatMap(lats_longs).add_to(map_obj)
    
    map_obj.save('heatmap.html')

create_heatmap()