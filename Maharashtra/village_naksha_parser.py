import os
import json
from pprint import pprint
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import ast
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

state_name = "Maharashtra"
states = {"Maharashtra": {"code": 27, "link": "https://mahabhunakasha.mahabhumi.gov.in"}}

def compile_extent_shapefile(state, file_path):

    with open(file_path, "r", encoding="utf8") as path:
        state_dict = json.loads(path.read())

    flat_villages = []
    for category in state_dict.keys():
        for district in state_dict[category].keys():
            for taluk in state_dict[category][district].keys():
                for village in state_dict[category][district][taluk].keys():
                    village_obj = state_dict[category][district][taluk][village]
                    flat_villages.append([category, district, taluk, village, village_obj["giscode"], village_obj["extent"]])

    df = pd.DataFrame(flat_villages, columns=["category", "district", "taluk", "village", "giscode", "extent"])
    df["geometry"] = df.apply(lambda x: Polygon([(x["extent"][0], x["extent"][2]), (x["extent"][0], x["extent"][3]), (x["extent"][1], x["extent"][3]), (x["extent"][1], x["extent"][2])]) if (len(x["extent"]) >= 4 and x["extent"][3] is not None) else None, axis=1)
    df = df.set_geometry('geometry')
    df.drop(["extent"], axis=1, inplace=True)
    df = df.set_crs('epsg:4326')
    df.to_file("./datasets/village_extents_corrected.shp")

    return df


def compile_plots_shapefile(state, file_list, edf):

    gdf = []
    for path in tqdm(file_list):

        plot_dfs = []

        try:
            with open(f"./{state}/{path}", "r") as file_path:
                village_dict = json.loads(file_path.read())
        except:
            print(f"Failed to open {path}")
            continue

        plot_dfs.append(gpd.GeoDataFrame.from_dict(village_dict['plots'], orient="index"))

        df = pd.concat(plot_dfs, ignore_index=True)
        if df.empty:
            print("No plots found.")
            continue

        try:
            df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
            df = df.set_geometry('geometry')

            df.set_crs("epsg:32643", inplace=True)
            df["giscode"] = path[:-5]

            gdf.append(df)
        except:
            print("204", path.split(".")[0])

    for district in tqdm(edf["district"].apply(lambda x: x[:3]).unique()):

        district_edf = edf[edf["district"].apply(lambda x: x[:3]) == district]
        district_dfs = []

        for df in gdf:
            if df.loc[0, "giscode"] in district_edf["giscode"].values:
                district_dfs.append(df)

        if not district_dfs:
            continue
        
        villages = pd.concat(district_dfs, ignore_index=True).drop(["owner_plots", "extent"], axis=1)
        villages = villages.to_crs('epsg:4326')

        merged = pd.merge(villages, district_edf, on="giscode", how="left")
        merged["geometry"] = merged["geometry_x"]
        merged.set_geometry('geometry', inplace=True)
        merged.drop(["geometry_x", "geometry_y"], axis=1, inplace=True)

        merged["link"] = merged["link"].apply(lambda x: x.split('href="')[1].split('>Map')[0].strip()[:-1])
        merged.to_file(f"./datasets/MH/{district.split(',')[0]}.shp")


    # villages = pd.concat(gdf, ignore_index=True).drop(["owner_plots", "extent"], axis=1)
    # villages = villages.to_crs('epsg:4326')

    # villages["link"] = villages["link"].apply(lambda x: x.split('href="')[1].split('>Map')[0].strip()[:-1])
    # villages.to_file("./datasets/villages.shp")

    # return villages


if __name__ == "__main__":

    extent_json = f"./{state_name}/village_extents_corrected.json"
    plot_files = [file for file in os.listdir(f"./{state_name}") if file.endswith(".json") and file.startswith("RVM")]

    # Populates ./datasets/village_extents.shp which is a map of all villages by rough extent
    # extents = compile_extent_shapefile(state_name, extent_json)
    extents = gpd.read_file("./datasets/village_extents.shp")

    # Populates ./datasets/villages.shp which is a map of all landholdings by exact polygons
    compile_plots_shapefile(state_name, plot_files, extents)
