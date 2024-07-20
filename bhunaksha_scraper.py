import os
import multiprocessing
import requests
import json
import random
from pprint import pprint
from tqdm import tqdm

states = {"Maharashtra": {"code": 27, "link": "https://mahabhunakasha.mahabhumi.gov.in"}}
cookies = {'geNPRu9S': '2902e030657ed2f0eb10d972e8d807ccb3eae48e884f68cfe858e4c228a54da3', "JSESSIONID": '296D8A332894DA04B436AE0AE4DC5F45'}

possible_headers = [
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
]


def grab_levels_json(session, state, codes):

    url = states[state]["link"] + "/rest/VillageMapService/ListsAfterLevelGeoref"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": states[state]["link"],
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"] + "/27/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&level=0&codes={codes}&hasmap=true"

    try:
        # Return the html if successful
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.text
        else:
            # Return an error code if not
            print(f"Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"Failed to download data from: {url}, error: {e}")
        return 0


def recursive_grab(session, state, level, codes, level_dict):
    all_levels = json.loads(grab_levels_json(session, state, codes))
    this_level = [(x['code'], x['value']) for x in all_levels[level]]

    if level == 3:
        print(level, this_level)
        for value in this_level:
            level_dict[",".join(value)] = {}
        return level_dict
    if level < 3:
        for value in this_level:
            level_dict[",".join(value)] = {}
            recursive_grab(session, state, level+1, codes+value[0]+"%2C", level_dict[",".join(value)])

    return level_dict


def construct_village_json(state):

    # Scrape the names of districts, taluks, etc.
    with requests.Session() as session:

        level_data = recursive_grab(session, state, 0, "", {})
        with open(f"./{state}/villages.json", "w") as file:
            json.dump(level_data, file)


def grab_and_parse_extent(session, state, giscode):

    url = states[state]["link"] + "/rest/MapInfo/getVVVVExtentGeoref"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": states[state]["link"],
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"] + "/27/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&giscode={giscode}&srs=4326"

    try:
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        # Parse and return the successful response
        if response.status_code == 200:
            data = json.loads(response.text)
            return {"giscode": giscode, "extent": [data["xmax"], data["xmin"], data["ymax"], data["ymin"]]}
        else:
            # Return an error code if not
            print(f"Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"Failed to download data from: {url}, error: {e}")
        return 0


def populate_village_extent(state, json_path):

    with open(json_path, "r", encoding="utf8") as file:
        data = json.load(file)

    with requests.Session() as session:

        for category in data.keys():
            cat_code = category.split(",")[0]
            for district in tqdm(data[category].keys()):
                dist_code = district.split(",")[0]
                for taluk in data[category][district].keys():
                    tal_code = taluk.split(",")[0]
                    for village in data[category][district][taluk].keys():
                        vil_code = village.split(",")[0]
                        map = "VM" if cat_code == "R" else "CM"

                        extents = grab_and_parse_extent(session, state, "".join([cat_code, map, dist_code, tal_code, vil_code]))
                        data[category][district][taluk][village] = extents

            with open(f"./{state}/village_extents.json", "w") as file:
                json.dump(data, file)


def grab_plot_numbers(session, state, giscode):

    url = states[state]["link"] + "/rest/VillageMapService/kidelistFromGisCodeMH"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": states[state]["link"],
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"] + "/27/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&logedLevels={giscode}"

    try:
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        # Parse and return the successful response
        if response.status_code == 200:
            data = json.loads(response.text)
            return {plot: {} for plot in data}
        else:
            # Return an error code if not
            print(f"Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"Failed to download data from: {url}, error: {e}")
        return 0


def populate_plots(state, json_path):

    with open(json_path, "r", encoding="utf8") as file:
        data = json.load(file)

    with requests.Session() as session:

        for category in data.keys():
            cat_code = category.split(",")[0]
            for district in tqdm(data[category].keys()):
                dist_code = district.split(",")[0]
                for taluk in data[category][district].keys():
                    tal_code = taluk.split(",")[0]
                    for village in data[category][district][taluk].keys():
                        vil_code = village.split(",")[0]
                        map = "VM" if cat_code == "R" else "CM"

                        plot_nums = grab_plot_numbers(session, state, "".join([cat_code, map, dist_code, tal_code, vil_code]))
                        data[category][district][taluk][village]["plots"] = plot_nums

                with open(f"./{state}/plots.json", "w") as file:
                    json.dump(data, file)


def grab_and_parse_plot_info(session, state, plot, giscode):

    url = states[state]["link"] + "/rest/MapInfo/getPlotInfo"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": states[state]["link"],
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"] + "/27/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&giscode={giscode}&plotno={plot}&srs=4326"

    try:
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        # Parse and return the successful response
        if response.status_code == 200:
            data = json.loads(response.text)
            return {"id": data["plotid"], "area": data["area"], "info": data["info"], "link": data["infoLinks"], "geometry": data["the_geom"], "owner_plots": data["ownerplots"]}
        else:
            # Return an error code if not
            print(f"PID: {os.getpid()}, Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"PID: {os.getpid()}, Failed to download data from: {url}, error: {e}")
        return ""


def grab_and_parse_plot_extent(session, state, plotid, giscode):

    url = states[state]["link"] + "/rest/MapInfo/getExtentGeoref"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": states[state]["link"],
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"] + "/27/index.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&giscode={giscode}&plotid={plotid}&srs=4326"

    try:
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        # Parse and return the successful response
        if response.status_code == 200:
            data = json.loads(response.text)
            return [data["xmax"], data["xmin"], data["ymax"], data["ymin"]]
            # return {plot: {} for plot in data}
        else:
            # Return an error code if not
            print(f"PID: {os.getpid()}, Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"PID: {os.getpid()}, Failed to download data from: {url}, error: {e}")
        return ""


def populate_taluk_plots(state, taluk, cat_code, dist_code, tal_code):

    map = "VM" if cat_code == "R" else "CM"
    output_path = f"./{state}/{cat_code}{map}{dist_code}{tal_code}.json"
    if os.path.exists(output_path):
        return

    with requests.Session() as session:

        for village in tqdm(taluk.keys()):
            vil_code = village.split(",")[0]

            for plot in taluk[village]["plots"].keys():
                plot_info = grab_and_parse_plot_info(session, state, plot, "".join([cat_code, map, dist_code, tal_code, vil_code]))
                plot_info["extent"] = grab_and_parse_plot_extent(session, state, plot_info["id"], "".join([cat_code, map, dist_code, tal_code, vil_code]))
                taluk[village]["plots"][plot] = plot_info

    with open(output_path, "w") as file:
        json.dump(taluk, file)


def populate_plot_info(state, json_path):

    with open(json_path, "r", encoding="utf8") as file:
        data = json.load(file)

    mp_tasks = []
    for category in data.keys():
        cat_code = category.split(",")[0]
        for district in data[category].keys():
            dist_code = district.split(",")[0]
            for taluk in data[category][district].keys():
                tal_code = taluk.split(",")[0]

                mp_tasks.append((state, data[category][district][taluk], cat_code, dist_code, tal_code))
                # populate_district_plots(state, data[category][district], cat_code, dist_code)

    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        pool.starmap(populate_taluk_plots, mp_tasks)


if __name__ == "__main__":

    state = "Maharashtra"

    # Grab the names and codes for all districts, villages, etc.
    # construct_village_json(state)
    # populate_village_extent(state, f"./{state}/villages.json")
    # populate_plots(state, f"./{state}/village_extents.json")
    populate_plot_info(state, f"./{state}/plots.json")
