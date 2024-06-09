import pandas as pd
import os
import folium


path = r"Unpack"
files = [path+'\\'+each for each in os.listdir(path) if each.endswith('.csv')]
file = files[-1]
print(file)
df = pd.read_csv(file)
count_rows = len(df['radio_status.rssi'].dropna())
df.fillna(0)
anomaly_gps_lon = [ i for i in df['sensor_gps.lon']]
anomaly_gps_lat = [ i for i in df['sensor_gps.lat']]

# Конвертация координат
df = pd.read_csv(file)
df_copy = df
df = df[['vehicle_gps_position.lat', 'vehicle_gps_position.lon']].dropna()
df['vehicle_gps_position.lat'] = df['vehicle_gps_position.lat'] / 10000000
df['vehicle_gps_position.lon'] = df['vehicle_gps_position.lon'] / 10000000

# Создание карты с центром в первой точке
map_center = [df['vehicle_gps_position.lat'].iloc[0], df['vehicle_gps_position.lon'].iloc[0]]
mymap = folium.Map(location=map_center, zoom_start=15, attributionControl = 0)
# # Добавление точек на карту
lt = 0
for idx, row in df.iterrows():

    if idx < count_rows and df_copy['radio_status.rxerrors'][idx] != 0:
        
        
        folium.Marker(
            location=[df_copy['sensor_gps.lat'][idx] / 10000000, df_copy['sensor_gps.lon'][idx] / 10000000],
            popup=f"""<b>Код ошибки приёма:</b> {df_copy['radio_status.rxerrors'][idx]}<br>
            <b>Сила синала:</b> {df_copy['radio_status.rssi'][idx]}<br>
            <b>Уровень удалённых шумов:</b> {df_copy['radio_status.remote_noise'][idx]}<br>
            <b>Координаты:</b> {df_copy['sensor_gps.lat'][idx]}, {df_copy['sensor_gps.lon'][idx]}
            """,
            icon=folium.Icon(color='red')
        ).add_to(mymap)
        lt = idx


    if row['vehicle_gps_position.lat'] in anomaly_gps_lat and row['vehicle_gps_position.lon'] in anomaly_gps_lon:
        pass
    else:
        folium.Marker(
            location=[row['vehicle_gps_position.lat'], row['vehicle_gps_position.lon']],
            popup=f"""OK<br>
            <b>Координаты:</b> {df_copy['sensor_gps.lat'][idx]}, {df_copy['sensor_gps.lon'][idx]}"""
        ).add_to(mymap)
print(lt)
# Сохранение карты в HTML файл
mymap.save(f"map.html")
mymap