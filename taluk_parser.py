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


if __name__ == "__main__":

    state = "Maharashtra"

    files = os.listdir(f"./{state}")
    files = [file for file in files if file.endswith(".json") and file.startswith("RVM")]

    gdf = []
    for path in files:

        print(path)

        with open(f"./{state}/{path}", "r") as file_path:
            taluk_dict = json.loads(file_path.read())

        for taluk in tqdm(taluk_dict):

            village_dfs = []
            for village in taluk_dict[taluk]:
                village_dfs.append(gpd.GeoDataFrame.from_dict(taluk_dict[taluk][village]['plots'], orient="index"))

            df = pd.concat(village_dfs, ignore_index=True)
            if df.empty:
                continue

            df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
            df = df.set_geometry('geometry')

            gdf.append(df)

    #  = gpd.read_file("https://gist.githubusercontent.com/planemad/d347ad7485344fb0ba4b470721825427/raw/4c683c9e1c46bc7373dc3df34202080e1a69c6e3/india-district-imd.geojson")
    taluks = pd.concat(gdf, ignore_index=True).drop(["owner_plots", "extent"], axis=1)
    taluks.to_file("./taluks.shp")

    ax = taluks.plot(column="area", cmap="viridis")
    ax.set_xlim(150000, 440000)
    plt.show()
