import pandas as pd
import matplotlib.pyplot as plt
import json

with open("./Maharashtra/village_extents.json", "r", encoding="utf-8") as file_path:
    extents = json.loads(file_path.read())

print(extents["R,Rural"].keys())

for taluk in extents["R,Rural"]["08,वर्धा"].keys():
    for village in extents["R,Rural"]["08,वर्धा"][taluk].keys():
        if extents["R,Rural"]["08,वर्धा"][taluk][village]["extent"][0] and extents["R,Rural"]["08,वर्धा"][taluk][village]["extent"][0] < 74:
            extents["R,Rural"]["08,वर्धा"][taluk][village]["extent"][0] += 6
            extents["R,Rural"]["08,वर्धा"][taluk][village]["extent"][1] += 6
            
for taluk in extents["R,Rural"]["09,नागपूर"].keys():
    for village in extents["R,Rural"]["09,नागपूर"][taluk].keys():
        if extents["R,Rural"]["09,नागपूर"][taluk][village]["extent"][0] and extents["R,Rural"]["09,नागपूर"][taluk][village]["extent"][0] < 74:
            extents["R,Rural"]["09,नागपूर"][taluk][village]["extent"][0] += 6
            extents["R,Rural"]["09,नागपूर"][taluk][village]["extent"][1] += 6
            
for taluk in extents["R,Rural"]['10,भंडारा'].keys():
    for village in extents["R,Rural"]['10,भंडारा'][taluk].keys():
        if extents["R,Rural"]['10,भंडारा'][taluk][village]["extent"][0] and extents["R,Rural"]['10,भंडारा'][taluk][village]["extent"][0] < 76:
            extents["R,Rural"]['10,भंडारा'][taluk][village]["extent"][0] += 6
            extents["R,Rural"]['10,भंडारा'][taluk][village]["extent"][1] += 6
            
for taluk in extents["R,Rural"]['11,गोंदिया'].keys():
    for village in extents["R,Rural"]['11,गोंदिया'][taluk].keys():
        if extents["R,Rural"]['11,गोंदिया'][taluk][village]["extent"][0] and extents["R,Rural"]['11,गोंदिया'][taluk][village]["extent"][0] < 76:
            extents["R,Rural"]['11,गोंदिया'][taluk][village]["extent"][0] += 6
            extents["R,Rural"]['11,गोंदिया'][taluk][village]["extent"][1] += 6
           
for taluk in extents["R,Rural"]['12,गडचिरोली'].keys():
    for village in extents["R,Rural"]['12,गडचिरोली'][taluk].keys():
        if extents["R,Rural"]['12,गडचिरोली'][taluk][village]["extent"][0] and extents["R,Rural"]['12,गडचिरोली'][taluk][village]["extent"][0] < 76:
            extents["R,Rural"]['12,गडचिरोली'][taluk][village]["extent"][0] += 6
            extents["R,Rural"]['12,गडचिरोली'][taluk][village]["extent"][1] += 6
 
for taluk in extents["R,Rural"]['13,चंद्रपूर'].keys():
    for village in extents["R,Rural"]['13,चंद्रपूर'][taluk].keys():
        if extents["R,Rural"]['13,चंद्रपूर'][taluk][village]["extent"][0] and extents["R,Rural"]['13,चंद्रपूर'][taluk][village]["extent"][0] < 76:
            extents["R,Rural"]['13,चंद्रपूर'][taluk][village]["extent"][0] += 6
            extents["R,Rural"]['13,चंद्रपूर'][taluk][village]["extent"][1] += 6
 
for taluk in extents["R,Rural"]['14,यवतमाळ'].keys():
    for village in extents["R,Rural"]['14,यवतमाळ'][taluk].keys():
        if extents["R,Rural"]['14,यवतमाळ'][taluk][village]["extent"][0] and extents["R,Rural"]['14,यवतमाळ'][taluk][village]["extent"][0] < 76.5:
            extents["R,Rural"]['14,यवतमाळ'][taluk][village]["extent"][0] += 6
            extents["R,Rural"]['14,यवतमाळ'][taluk][village]["extent"][1] += 6
 
with open("./Maharashtra/village_extents_corrected.json", "w", encoding="utf-8") as file_path:
    json.dump(extents, file_path, ensure_ascii=False)

'''giscodes, latlongs = [], []
for taluk in extents["R,Rural"]["08,वर्धा"].keys():
    for village in extents["R,Rural"]["08,वर्धा"][taluk].keys():
        village_obj = extents["R,Rural"]["08,वर्धा"][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<74 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]["09,नागपूर"].keys():
    for village in extents["R,Rural"]["09,नागपूर"][taluk].keys():
        village_obj = extents["R,Rural"]["09,नागपूर"][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<74 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]['10,भंडारा'].keys():
    for village in extents["R,Rural"]['10,भंडारा'][taluk].keys():
        village_obj = extents["R,Rural"]['10,भंडारा'][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<76 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]['11,गोंदिया'].keys():
    for village in extents["R,Rural"]['11,गोंदिया'][taluk].keys():
        village_obj = extents["R,Rural"]['11,गोंदिया'][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<76 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]['12,गडचिरोली'].keys():
    for village in extents["R,Rural"]['12,गडचिरोली'][taluk].keys():
        village_obj = extents["R,Rural"]['12,गडचिरोली'][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<76 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]['13,चंद्रपूर'].keys():
    for village in extents["R,Rural"]['13,चंद्रपूर'][taluk].keys():
        village_obj = extents["R,Rural"]['13,चंद्रपूर'][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<76 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()

giscodes, latlongs = [], []
for taluk in extents["R,Rural"]['14,यवतमाळ'].keys():
    for village in extents["R,Rural"]['14,यवतमाळ'][taluk].keys():
        village_obj = extents["R,Rural"]['14,यवतमाळ'][taluk][village]
        giscodes.append(village_obj["giscode"])
        latlongs.append((village_obj["extent"][0], village_obj["extent"][2]))

df = pd.DataFrame({"giscode": giscodes, "longs": [x[0] for x in latlongs], "lats": [x[1] for x in latlongs]})
df["longs"] = df["longs"].apply(lambda x: x+6 if x<76.5 else x)
print(df.head())

plt.scatter(df["longs"], df["lats"])
plt.show()'''
