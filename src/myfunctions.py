from pymongo import MongoClient
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster
import requests
from pymongo import GEOSPHERE
import json
from dotenv import load_dotenv
from cartoframes.viz import Map, Layer, popup_element
import os

def design_comps():
    client = MongoClient("localhost:27017")
    db= client["Ironhack"]
    companies=db.get_collection("companies")

    # show me all the design companies according to the category in the database
    query=[{"category_code":"design"},{"number_of_employees":{"$gte":10}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    comp_list=list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1))

    # get companies that have design in the name
    query=[{"name":{"$regex":".*design.*"}},{"number_of_employees":{"$gte":10}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    comp_list.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # get the largest companies that have design in one of the "tag_list" entries
    query=[{"tag_list":{"$regex":".*design.*"}},{"number_of_employees":{"$gte":10}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    comp_list.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # get the largest companies in the web space
    query=[{"category_code":"web"},{"number_of_employees":{"$gte":10}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    comp_list.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    # get the largest startups
    query=[{"founded_year":{"$gte":2009}},{"number_of_employees":{"$gte":10}}]
    projection={"name":1,"category_code":1,"total_money_raised":1,"number_of_employees":1,"offices.country_code":1,"offices.city":1, "offices.latitude":1,"offices.longitude":1,"_id":0}
    comp_list.extend(list(companies.find({"$and": query}, projection).limit(500).sort("number_of_employees",-1)))

    df=pd.DataFrame(comp_list)

    # put the dictionary elemenst into separate rows
    df=df.explode('offices')
    df.reset_index(inplace=True,drop=True)

    def office_country(dict_):
        try:
            if 'country_code' in dict_.keys():
                country=dict_['country_code']
            elif type(dict_)==str:
                country=dict__
            else:
                country=np.nan
        except:
            country=np.nan
        return country

    def office_city(dict_):
        try:
            if 'city' in dict_.keys():
                city=dict_['city']
            elif type(dict_)==str:
                city=dict__
            else:
                city=np.nan
        except:
            city=np.nan
        return city

    def office_lat(dict_):
        try:
            if 'latitude' in dict_.keys():
                lat=dict_['latitude']
            elif type(dict_)==str:
                lat=dict__
            else:
                lat=np.nan
        except:
            lat=np.nan
        return lat

    def office_long(dict_):
        try:
            if 'longitude' in dict_.keys():
                long=dict_['longitude']
            elif type(dict_)==str:
                long=dict__
            else:
                long=np.nan
        except:
            long=np.nan
        return long

    df['country']=df['offices'].apply(office_country)
    df['city']=df['offices'].apply(office_city)
    df['lat']=df['offices'].apply(office_lat)
    df['long']=df['offices'].apply(office_long)

    df2=df.dropna(subset=['city','lat'])
    df3=df2.drop(columns=['offices'])
    df3.reset_index(inplace=True,drop=True)
    df3.drop(df3[df3['total_money_raised'] == '$0'].index, inplace=True)
    return df3

#Read, clean and sort the country data
def get_country_data():

    df_education=pd.read_csv("./input/education.csv", encoding='ISO-8859-1',header=None, names=['Code','Year','Education'])
    df_education.drop(axis=0,index=0, inplace=True)
    df_education['Year']=df_education['Year'].astype(int)
    df_education['Education']=df_education['Education'].astype(float)
    df_healthcare=pd.read_csv("./input/healthcare.csv", encoding='ISO-8859-1')
    df_healthcare['Year']=df_healthcare['Year'].astype(int)
    df_corruption=pd.read_csv("./input/corruption.csv", encoding='ISO-8859-1')
    df_corruption['Year']=df_corruption['Year'].astype(int)
    df_homicide=pd.read_csv("./input/homicide_clean.csv", encoding='ISO-8859-1')
    df_homicide['Year']=df_homicide['Year'].astype(int)

    df_quality=pd.merge(df_education,df_healthcare,on=['Code','Year'])
    df_quality=pd.merge(df_quality,df_corruption,on=['Code','Year'])
    df_quality=pd.merge(df_quality,df_homicide,on=['Code','Year'])
    df_quality.drop(columns=['Entity_x','Entity_y'],inplace=True)
    df_quality.rename(columns={"Entity":"Country"},inplace=True)
    df_quality=df_quality[['Code','Country','Year','Homicide rate','Corruption','Education','Healthcare expense % GDP']]

    df_quality['hom_st']=(df_quality['Homicide rate'].mean()-df_quality['Homicide rate'])/df_quality['Homicide rate'].std()
    df_quality['corr_st']=(df_quality['Corruption']-df_quality['Corruption'].mean())/df_quality['Corruption'].std()
    df_quality['edu_st']=(df_quality['Education']-df_quality['Education'].mean())/df_quality['Education'].std()
    df_quality['heal_st']=(df_quality['Healthcare expense % GDP']-df_quality['Healthcare expense % GDP'].mean())/df_quality['Healthcare expense % GDP'].std()

    df_quality['hom_rank']=df_quality['hom_st'].rank(axis=0, ascending=False)
    df_quality['corr_rank']=df_quality['corr_st'].rank(axis=0, ascending=False)
    df_quality['edu_rank']=df_quality['edu_st'].rank(axis=0, ascending=False)
    df_quality['heal_rank']=df_quality['heal_st'].rank(axis=0, ascending=False)

    df_quality['comb_rank']=df_quality['hom_rank']*0.25+df_quality['corr_rank']*0.25+df_quality['edu_rank']*0.25+df_quality['heal_rank']*0.25

    df_quality['comb_rank_unique']=df_quality['comb_rank'].rank(axis=0, ascending=True)

    return df_quality

# filter your database for target companies
def filter_targets(df3, countries, top):
    df_target_comps=df3[df3['country'].isin(countries)]
    # select 3 top cities
    target_cities=df_target_comps['city'].value_counts()[:top]
    target_cities=list(target_cities.index)
    df_target_comps=df_target_comps[df_target_comps['city'].isin(target_cities)]
    df_target_comps=df_target_comps[(df_target_comps['name']!='Wahanda')]

    return df_target_comps, target_cities

# get the target city coordinates - average of the businesses
def get_city_coords(target_cities,df_target_comps):

    city_coords={"City":[],"Latitude":[],"Longitude":[]}
    for i in target_cities:
        lat=[]
        long=[]
        lat=df_target_comps[df_target_comps['city']==i]['lat'].sum()/len(df_target_comps[df_target_comps['city']==i])
        long=df_target_comps[df_target_comps['city']==i]['long'].sum()/len(df_target_comps[df_target_comps['city']==i])
        city_coords['City'].append(i)
        city_coords['Latitude'].append(lat)
        city_coords['Longitude'].append(long)

    df_cities=pd.DataFrame(city_coords)

    return df_cities

# get points of interest from Forsquare
def get_points_of_interest(y_lat,y_long,wishes):
    load_dotenv()
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    client_key=os.getenv("API_KEY")
    df_locations=pd.DataFrame(columns=['Name','Category','Latitude','Longitude','Distance','Address'])

    for keys, values in wishes.items():
        if type(values['cat_id'])==int:
            url = f"https://api.foursquare.com/v3/places/search?ll={y_lat}%2C{y_long}&radius={values['distance']}&categories={values['cat_id']}&sort={values['sort']}&limit=5"
        else:
            url = f"https://api.foursquare.com/v3/places/search?query={values['cat_id']}&ll={y_lat}%2C{y_long}&radius={values['distance']}&sort={values['sort']}&limit=5"
        headers = {
            "Accept": "application/json",
            "Authorization": client_key
        }

        response = requests.get(url, headers=headers)

        loc_name=[]
        cat_name=[]
        lat=[]
        long=[]
        distance=[]
        address=[]

        for i in range(len(response.json()["results"])):
            loc_name.append(response.json()["results"][i]['name'])
            try:
                cat_name.append(response.json()["results"][i]['categories'][0]['name'])
            except:
                cat_name.append('')
            lat.append(response.json()["results"][i]['geocodes']['main']['latitude'])
            long.append(response.json()["results"][i]['geocodes']['main']['longitude'])
            distance.append(response.json()["results"][i]['distance'])
            address.append(response.json()["results"][i]['location']['formatted_address'])

        loc_list=list(zip(loc_name, cat_name, lat, long, distance,address))
        df_loc=pd.DataFrame(loc_list,columns=['Name','Category','Latitude','Longitude','Distance','Address'])
        df_loc['Requirement']=keys
        df_loc
        df_locations=pd.merge(df_locations,df_loc,how='outer')
        time.sleep(1)
    
    return df_locations

def map_markers(map_1,df_loc):

    for index, row, in df_loc.iterrows():
        district={"location":[row["Latitude"], row["Longitude"]], "tooltip":row["Requirement"]}
        # 1. Education
        if row['Requirement']=='school':
            icon= Icon(color="red", prefix="fa", icon="graduation-cap", icon_color="black")
        # 2. Starbucks
        elif row['Requirement']=='starbucks':
            icon= Icon(color="green", prefix="fa", icon="coffee", icon_color="black")
        # 3. Bar
        elif row['Requirement']=='bar':
            icon= Icon(color="orange", prefix="fa", icon="glass", icon_color="black")
        # 4. Club
        elif row['Requirement']=='club':
            icon= Icon(color="purple", prefix="fa", icon="music", icon_color="black")
        # 5. Airport
        elif row['Requirement']=='Airport':
            icon= Icon(color="blue", prefix="fa", icon="plane", icon_color="black")    
        # 6. Vegan
        elif row['Requirement']=='vegan':
            icon= Icon(color="beige", prefix="fa", icon="leaf", icon_color="black")
        # 7. Basketball
        elif row['Requirement']=='basketball':
            icon= Icon(color="orange", prefix="fa", icon="futbol-o", icon_color="black")
        # 8. Pet grooming
        elif row['Requirement']=='pet grooming':
            icon= Icon(color="red", prefix="fa", icon="paw", icon_color="black")
        
        new_marker=Marker(icon=icon, **district)
        new_marker.add_to(map_1)

    return map_1
