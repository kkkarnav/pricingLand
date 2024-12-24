import os
import multiprocessing
import requests
import json
import random
from pprint import pprint
from tqdm import tqdm
from bs4 import BeautifulSoup

states = {"Odisha": {"code": 21, "link": "https://bhunakshaodisha.nic.in/"}}
districts = {"1": "https://app1bhunakshaodisha.nic.in/bhunaksha/",
             "2": "https://app1bhunakshaodisha.nic.in:8443/bhunaksha/",
             "3": "https://app4bhunakshaodisha.nic.in:8443/bhunaksha/",
             "4": "https://bhunakshaodisha.nic.in:8443/bhunaksha/",
             "5": "https://app3bhunakshaodisha.nic.in:8443/bhunaksha/",
             "6": "https://bhunakshaodisha.nic.in/bhunaksha/",
             "7": "https://app4bhunakshaodisha.nic.in/bhunaksha/",
             "8": "https://app4bhunakshaodisha.nic.in/bhunaksha/",
             "9": "https://app1bhunakshaodisha.nic.in:8443/bhunaksha/",
             "10": "https://app1bhunakshaodisha.nic.in/bhunaksha/",
             "11": "https://app2bhunakshaodisha.nic.in/bhunaksha/",
             "12": "https://app2bhunakshaodisha.nic.in:8443/bhunaksha/",
             "13": "https://bhunakshaodisha.nic.in/bhunaksha/",
             "14": "https://bhunakshaodisha.nic.in:8443/bhunaksha/", 
             "15": "https://app2bhunakshaodisha.nic.in:8443/bhunaksha/",
             "16": "https://app1bhunakshaodisha.nic.in/bhunaksha/",
             "17": "https://app4bhunakshaodisha.nic.in:8443/bhunaksha/",
             "18": "https://app4bhunakshaodisha.nic.in/bhunaksha/",
             "19": "https://bhunakshaodisha.nic.in:8443/bhunaksha/", 
             "20": "https://app3bhunakshaodisha.nic.in/bhunaksha/",
             "21": "https://bhunakshaodisha.nic.in/bhunaksha/",
             "22": "https://app2bhunakshaodisha.nic.in/bhunaksha/",
             "23": "https://app3bhunakshaodisha.nic.in/bhunaksha/",
             "24": "https://app3bhunakshaodisha.nic.in:8443/bhunaksha/",
             "25": "https://app1bhunakshaodisha.nic.in:8443/bhunaksha/",
             "26": "https://app3bhunakshaodisha.nic.in/bhunaksha/",
             "27": "https://app2bhunakshaodisha.nic.in/bhunaksha/",
             "28": "https://app3bhunakshaodisha.nic.in:8443/bhunaksha/",
             "29": "https://app4bhunakshaodisha.nic.in:8443/bhunaksha/",
             "30": "https://app2bhunakshaodisha.nic.in:8443/bhunaksha/"}
cookies = {"JSESSIONID": '7B5FFA7CBB6BE2FDE53A6FC6C78A5F75'}

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

def grab_districts_html(session, state, district_code):

    url = districts[district_code]
    
    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": states[state]["link"],
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }

    try:
        # Return the html if successful
        response = session.post(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.text
        else:
            # Return an error code if not
            print(f"Failed to download data from: {url}, status code: {response.status_code}", )
            return ""
    except Exception as e:
        print(f"Failed to download data from: {url}, error: {e}")
        return 0


def parse_districts_html(html):
    
    parsed_html = BeautifulSoup(html, 'html.parser')
    div = parsed_html.find("div", {"id": "village_selector"})
    select = div.find_all("select")[0]
    options = [option.text for option in select.find_all("option")]
    
    return options


def grab_levels_html(session, state, level, codes):

    url = districts[codes.split("%2C")[0]] + "ScalarDatahandler"
    
    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": districts[codes.split("%2C")[0]],
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"OP=2&level={level}&selections={codes}&state={states[state]['code']}"

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
        return ""


def parse_levels_html(html, level):
    
    parsed_html = BeautifulSoup(html, 'html.parser')
    div = parsed_html.find("div", {"id": f"div_level_{level}"})
    select = div.find_all("select")[0]
    options = [option.text for option in select.find_all("option")]
    
    return options


def recursive_grab(session, state, level, codes, level_dict):
    this_level = parse_levels_html(grab_levels_html(session, state, level, codes), level)
    
    if level == 5:
        for value in this_level:
            level_dict[value] = {}
        return level_dict
    
    if level < 5:
        for value in this_level:
            level_dict[value] = {}
            recursive_grab(session, state, level + 1, codes+"%2C"+value.split(" ")[0], level_dict[value])

    return level_dict


def construct_village_json(state):

    # Scrape the names of districts, taluks, etc.
    with requests.Session() as session:

        districts = []
        for district_index in tqdm(range(1, 31)):
            districts.extend(parse_districts_html(grab_districts_html(session, state, str(district_index))))
        
        districts = list(set(districts))
        print(districts)
        
        level_data = {}
        for district in tqdm(districts):
            level_data[district] = recursive_grab(session, state, 2, district.split(" ")[0], {})
        
        print(level_data)
        with open(f"./{state}/villages.json", "w") as file:
            json.dump(level_data, file)


def grab_and_parse_extent(session, state, district_code, giscode):

    url = districts[district_code] + "rest/MapInfo/getVVVVExtentGeoref"

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
    }
    post_data = f"state={states[state]['code']}&gisLevels={giscode}&srs=0"
    print(post_data)

    try:
        response = session.post(url, data=post_data, headers=headers, cookies=cookies)
        # Parse and return the successful response
        if response.status_code == 200:
            data = json.loads(response.text)
            return {"giscode": giscode, 
                    "extent": [data["xmax"], data["xmin"], data["ymax"], data["ymin"]], 
                    "last_updated": data["attribution"].split("Updated on :")[1].split("<br")[0]}
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

        for district in tqdm(data.keys()):
            dist_code = district.split(" ")[0]
            for taluk in data[district].keys():
                tal_code = taluk.split(" ")[0]
                for ri in data[district][taluk].keys():
                    ri_code = ri.split(" ")[0]
                    for village in data[district][taluk][ri].keys():
                        vil_code = village.split(" ")[0]

                        extents = grab_and_parse_extent(session, state, district.split(" ")[0], "%2C".join([dist_code, tal_code, ri_code, vil_code]))
                        data[district][taluk][ri][village] = extents
                        break
                    break
                break

    with open(f"./{state}/village_extents.json", "w") as file:
        json.dump(data, file)


if __name__ == "__main__":

    state = "Odisha"

    # This populates ./{state}/villages.json with the codes and names required to look up each village
    construct_village_json(state)

    # This populates ./{state}/village_extents.json with the rough (square) extents of each village
    # populate_village_extent(state, f"./{state}/villages.json")

    # This populates ./{state}/plots.json with the plot numbers
    # populate_plots(state, f"./{state}/plots.json")

    # This populates the ./{state} directory with .json files representing the plot info and extents for each village
    # populate_plot_info(state, f"./{state}/plots.json")
