import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from cartopy import crs as ccrs


def create_map():
    fig, wine_map = plt.subplots(figsize=(15, 15),
                                 subplot_kw={'projection': ccrs.PlateCarree()})
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world.plot(ax=wine_map, color="lightgrey")
    italy = world[(world.name == "Italy")]
    france = world[(world.name == "France")]
    germany = world[(world.name == "Germany")]
    us = world[(world.name == "United States of America")]
    spain = world[(world.name == "Spain")]
    switzerland = world[(world.name == "Switzerland")]
    ukraine = world[(world.name == "Ukraine")]
    england = world[(world.name == "United Kingdom")]
    peru = world[(world.name == "Peru")]
    wine_map.add_geometries(italy['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='red')
    wine_map.add_geometries(france['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='darkred')
    wine_map.add_geometries(germany['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='indianred')
    wine_map.add_geometries(us['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='mediumvioletred')
    wine_map.add_geometries(spain['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='palevioletred')
    wine_map.add_geometries(switzerland['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='skyblue')
    wine_map.add_geometries(ukraine['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='navy')
    wine_map.add_geometries(england['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='gold')
    wine_map.add_geometries(peru['geometry'], crs=ccrs.PlateCarree(),
                            facecolor='yellow')
    legendelement = [
        mpatches.Patch(color='red', label='Red Blend'),
        mpatches.Patch(color='darkred', label='Gewrztraminer'),
        mpatches.Patch(color='indianred', label='Riesling'),
        mpatches.Patch(color='mediumvioletred', label='Merlot'),
        mpatches.Patch(color='palevioletred', label='Tempranillo'),
        mpatches.Patch(color='skyblue', label='Most expensive country'),
        mpatches.Patch(color='navy', label='Cheapest country'),
        mpatches.Patch(color='gold', label='Most rated country'),
        mpatches.Patch(color='yellow', label='Underrated country'),
    ]
    wine_map.legend(handles=legendelement, ncol=2, mode="expand", loc=8)
    plt.title('Map of wines')
    plt.savefig('map_of_wines.png')
    plt.close()


def create_bar(statistics):
    statistics['wine'].pop('Madera')
    data_names, data_avg, data_min, data_max, data_score = [], [], [], [], []
    for key, value in statistics['wine'].items():
        data_names.append(key.encode('latin-1').decode('unicode-escape'))
        data_min.append(int(value['min_price']))
        data_max.append(int(value['max_price'])//10)
        data_avg.append(int(value['average_price']))
        data_score.append(int(value['average_score']))
    fig, (price_bar, score_bar) = plt.subplots(2, figsize=(15, 15))
    xs = range(len(data_names))
    price_bar.bar([x + 0.0 for x in xs], data_min, width=0.25,
                  color='lightskyblue', label='min_price')
    price_bar.bar([x + 0.25 for x in xs], data_avg, width=0.25,
                  color='slategray', label='average_price')
    price_bar.bar([x + 0.50 for x in xs], data_max, width=0.25,
                  color='midnightblue', label='max_price/10')
    price_bar.set_xticks([x + 0.25 for x in xs])
    price_bar.set_xticklabels(data_names)
    price_bar.set_ylabel('money')
    price_bar.set_title("Prices")
    price_bar.legend()
    score_bar.bar([x + 0.0 for x in xs], data_score, width=0.25,
                  color='lightskyblue', label='average_score')
    score_bar.set_ylim(78, 100)
    score_bar.axhline(statistics['lowest_score'], color='midnightblue',
                      label='lowest_score')
    score_bar.set_xticks(xs)
    score_bar.set_xticklabels(data_names)
    score_bar.set_ylabel('points')
    score_bar.set_title("Scores")
    score_bar.legend()
    plt.savefig('Bars_for_wine.png')
    plt.close()
