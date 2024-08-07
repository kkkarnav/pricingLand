import os
import json
from pprint import pprint
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import ast
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

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
    df.to_file("./village_extents.shp")


def compile_plots_shapefile(state, file_list):

    gdf = []
    for path in file_list:

        print(path)
        plot_dfs = []

        with open(f"./{state}/{path}", "r") as file_path:
            village_dict = json.loads(file_path.read())

        plot_dfs.append(gpd.GeoDataFrame.from_dict(village_dict['plots'], orient="index"))

        df = pd.concat(plot_dfs, ignore_index=True)
        if df.empty:
            print("No villages found.")
            continue

        df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
        df = df.set_geometry('geometry')
        df.set_crs("epsg:32643", inplace=True)
        df["giscode"] = path[:-5]

        gdf.append(df)

    villages = pd.concat(gdf, ignore_index=True).drop(["owner_plots", "extent"], axis=1)
    villages = villages.to_crs('epsg:4326')
    villages.to_file("./villages.shp")

    return villages


if __name__ == "__main__":

    state_name = "Maharashtra"
    extent_json = f"./{state_name}/village_extents.json"
    plot_files = os.listdir(f"./{state_name}")
    plot_files = [file for file in plot_files if file.endswith(".json") and file.startswith("RVM")]

    compile_extent_shapefile(state_name, extent_json)
    gdf = compile_plots_shapefile(state_name, plot_files)
    ax = gdf.plot(column="area", cmap="viridis")
    plt.show()
