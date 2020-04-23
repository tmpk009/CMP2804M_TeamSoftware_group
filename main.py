# MAIN PYTHON FILE
# Last modified by: Thomas Pike

# import flask module
from flask import Flask, render_template, request, jsonify
# import requests for apis
# documentation @ https://2.python-requests.org/en/master/
import requests
# import csv
import csv
import json
import time

# documentation @ https://pandas.pydata.org/docs/
import pandas as pd
# documentation @ https://matplotlib.org/3.2.1/contents.html
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import glob

# global vars
user_date = "2020-01"
file_num = "global"
lat = "global"
long = "global"
lat2 = "global"
long2 = "global"
lsoa = "global"
lsoa2 = "global"
mnths = "1"
latLong = "global"
name = "global"
graph1 = ""
graph2 = ""
exists = True
bestWorst="global"
highlow3="global"
recLat1="global"
recLat2="global"
recLat3="global"
recLong1="global"
recLong2="global"
recLong3="global"
recLtLn="global"
best1="global"
best2="global"
best3="global"
done=False

# create instance of flask called app
app = Flask(__name__)


# default page path
@app.route("/")
# web contents
def home():
    # renders web page
    return render_template("index.html")
# end of home()

@app.route("/index.html")
def index():
    # renders web page
    return render_template("index.html")
# end of index()



# !MAP!

@app.route("/Map.html")
def map():
    # renders web page
    return render_template("Map.html")
# end of map()

# deals with GET and POST requests
@app.route("/mapjs", methods=['GET', 'POST'])
def mapjs():
    # use of global vars
    global latLong
    global lat
    global long

    # POST REQUEST FOR TESTING
    # POST request
    if request.method == 'POST':
        # confirms json received by printing to local console
        print('Incoming..')
        print(request.get_json(force=True))# parse as JSON

        # creates python object of latLong
        latLong = request.get_json(force=True)

        # takes latitude and longitude from json passed from web
        lat = latLong['ourLat']
        long = latLong['ourLong']

        # requires specific parameters for 'date', 'latitude', 'longitude'
        # grabs all crime "nearby" in the given month
        # hands web file the json variable
        time = '2020-01'
        info = {'date': time, 'lat': lat, 'lng': long}
        specific = requests.get("https://data.police.uk/api/crimes-at-location", params=info)

        # response from api called 'inp'
        inp = specific.text

        if (inp == "[]"):
            inp = "No data for this area"

        # returns 'inp' to the web console along with confirmation of success
        return inp, 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
# end of mapjs()



# !COMPARE!

@app.route("/Compare.html")
def compare():
     #renders web page
    return render_template("Compare.html")
# end of compare()

# deals with GET and POST requests
@app.route("/comparejs", methods=['GET', 'POST'])
def comparejs():
    global mnths

    # handles POST REQUEST from js
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json(force=True)) # parse as JSON
        mon = request.get_json(force=True)

        # gets months from web
        mnths = mon['num']

        # removes currently existing csv file
        fileList = glob.glob('police_data*.csv')

        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                print("Error deleting file ", filePath)

        comparefil()
        create()

        return 'OK', 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
# end of comparejs()

# for map 1
@app.route("/comparejs1", methods=['GET', 'POST'])
def comparejs1():
    global mnths
    global lat
    global long
    global lsoa
    global exists

    # handles POST REQUEST from js
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json(force=True)) # parse as JSON
        mp = request.get_json(force=True)

        lat = mp['ourLat']
        long = mp['ourLong']
        lsoa = mp['ls']


        try:
            f = open("police_data1.csv")
        except IOError:
            message = "Please select a timeframe"
            print(message)
            exists = False
        finally:
            f.close()

        if (exists == True):
            loc1()

        exists = True

        return 'OK', 200

    # sleeps the program to stop the file being deleted before being displayed
    time.sleep(2)
    fileList = glob.glob('static/IMAGES/compare1/graph*.png')

    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error deleting file ", filePath)
    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
# end of comparejs1()

# for map2
@app.route("/comparejs2", methods=['GET', 'POST'])
def comparejs2():
    global mnths
    global lat2
    global long2
    global lsoa2
    global exists

    # handles POST REQUEST from js
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json(force=True)) # parse as JSON
        mp = request.get_json(force=True)

        lat2 = mp['ourLat']
        long2 = mp['ourLong']
        lsoa2 = mp['ls']


        try:
            f = open("police_data1.csv")
        except IOError:
            message = "Please select a timeframe"
            print(message)
            exists = False
        finally:
            f.close()

        if (exists == True):
            loc2()

        exists = True

        return 'OK', 200

    time.sleep(2)
    fileList = glob.glob('static/IMAGES/compare2/graph*.png')

    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error deleting file ", filePath)
    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)  # serialize and use JSON headers
# end of comparejs2()

# gets specified time frame for compare, these will be passed to compare_vis to filtered to the two specified lcoations
def comparefil():
    # mnths come from the web form

    # vars
    global file_num
    file_num = 1
    month_count = 1

    # 1 mnth
    if (mnths == "1"):
        csv_delete()

    # 3 mnths
    if (mnths == "3"):
        while (month_count <= 3):
            if (month_count == 1):
                file_num = 1
                user_date = "2020-01"
            if (month_count == 2):
                file_num = 2
                user_date = "2019-12"
            if (month_count == 3):
                file_num = 3
                user_date = "2019-11"
            csv_delete()
            month_count += 1

    # 6mnths
    elif (mnths == "6"):
        while (month_count <= 6):
            if (month_count == 1):
                file_num = 1
                user_date = "2020-01"
            elif (month_count == 2):
                file_num = 2
                user_date = "2019-12"
            elif (month_count == 3):
                file_num = 3
                user_date = "2019-11"
            elif (month_count == 4):
                file_num = 4
                user_date = "2019-10"
            elif (month_count == 5):
                file_num = 5
                user_date = "2019-09"
            elif (month_count == 6):
                file_num = 6
                user_date = "2019-08"
            csv_delete()
            month_count += 1

    # year
    elif (mnths == "12"):
        while (month_count <= 12):
            if (month_count == 1):
                file_num = 1
                user_date = "2020-01"
            elif (month_count == 2):
                file_num = 2
                user_date = "2019-12"
            elif (month_count == 3):
                file_num = 3
                user_date = "2019-11"
            elif (month_count == 4):
                file_num = 4
                user_date = "2019-10"
            elif (month_count == 5):
                file_num = 5
                user_date = "2019-09"
            elif (month_count == 6):
                file_num = 6
                user_date = "2019-08"
            elif (month_count == 7):
                file_num = 7
                user_date = "2019-07"
            elif (month_count == 8):
                file_num = 8
                user_date = "2019-06"
            elif (month_count == 9):
                file_num = 9
                user_date = "2019-05"
            elif (month_count == 10):
                file_num = 10
                user_date = "2019-04"
            elif (month_count == 11):
                file_num = 11
                user_date = "2019-03"
            elif (month_count == 12):
                file_num = 12
                user_date = "2019-02"
            csv_delete()
            month_count += 1
# end of comparefil()

# merges all police data csvs
def create():


    extension = 'csv'
    all_files = [i for i in glob.glob('police_data*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    # export to csv
    combined_csv.to_csv("frequency.csv", index = False, encoding='utf-8-sig')


    # first location
    df1 = pd.read_csv("frequency.csv", header=0, escapechar='\\')

    df1.columns = df1.columns.str.strip().str.lower().str.replace(' ', '_')

    # get frequencies
    valu = df1['crime_type'].value_counts()
    # print frequencies for testing reasons
    print(valu)

    names = df1['lsoa_name'].value_counts()
    print(names)

    os.remove("frequency.csv")

# end of create()

# generates chart for first map
def loc1():
    global graph1
    global lsoa
    extension = 'csv'
    all_files = [i for i in glob.glob('police_data*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    # export to csv
    combined_csv.to_csv("frequency1.csv", index=False, encoding='utf-8-sig')

    # second location
    df2 = pd.read_csv("frequency1.csv", header=0, escapechar='\\')

    df2.columns = df2.columns.str.strip().str.lower().str.replace(' ', '_')

    filt = df2.lsoa_name.str.contains(lsoa)

    comp1 = df2[filt]

    # get frequencies
    valu = comp1["crime_type"].value_counts()
    crimes = comp1["crime_type"].value_counts().keys()

    #create graph
    plt.title("Crimes in specified area")
    plt.ylabel("Number of crime type committed")
    plt.xlabel("Crime")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.bar(crimes, valu)
    plt.tight_layout()
    #plt.show()
    plt.savefig('static/IMAGES/compare1/graph1.png', pad_inches=0.1)


    os.remove("frequency1.csv")

#end of loc1()

#generates chart for second map
def loc2():
    global graph2
    global lsoa2
    extension = 'csv'
    all_files = [i for i in glob.glob('police_data*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    # export to csv
    combined_csv.to_csv("frequency2.csv", index=False, encoding='utf-8-sig')

    # second location
    df3 = pd.read_csv("frequency2.csv", header=0, escapechar='\\')

    df3.columns = df3.columns.str.strip().str.lower().str.replace(' ', '_')

    filt = df3.lsoa_name.str.contains(lsoa2)

    df4 = df3[filt]

    # get frequencies
    valu = df4["crime_type"].value_counts()
    crimes = df4["crime_type"].value_counts().keys()

    # create graph
    plt.title("Crimes in specified area")
    plt.ylabel("Number of crime type committed")
    plt.xlabel("Crime")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.bar(crimes, valu)
    #plt.show()
    plt.savefig('static/IMAGES/compare2/graph2.png', pad_inches=0.1)

    os.remove("frequency2.csv")
# end of loc2()



# !RECOMMEND!

@app.route("/Recommend.html")
def recommend():

    # renders web page
    return render_template("Recommend.html")
#end of recommend()

#deals with POST and GET requests
@app.route("/recommendjs", methods=['GET', 'POST'])
def recommendjs():
    global name
    global bestWorst

    global highlow3
    global done
    # handles POST REQUEST from js
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json(force=True))  # parse as JSON
        rec = request.get_json(force=True)

        name = rec['name']

        recommendfil()
        name=""
        done = True
        return str(highlow3), 200

    time.sleep(2)
    fileList = glob.glob('static/IMAGES/recommend/graph*.png')
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error deleting file ", filePath)
    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)
# end of recommendjs()

#deals with POST and GET requests
@app.route("/recommendjs2", methods=['GET', 'POST'])
def recommendjs2():
    global name
    global bestWorst
    global  highlow3
    global recLat1
    global recLat2
    global recLat3
    global recLtLn
    global done

    # handles POST REQUEST from js
    if request.method == 'POST':
        print('Incoming..')
        print(request.get_json(force=True))  # parse as JSON
        rec = request.get_json(force=True)

        while(done==False):
            if(done == False):
                time.sleep(1)

        done = False
        return recLtLn, 200

    # GET request
    else:
        message = {'greeting': 'Hello from Flask!'}
        return jsonify(message)
# end of recommendjs()

# generate csv and chart
def recommendfil():
    file_num = 1
    # creates one file to be sorted by data_vis
    global mnths
    global bestWorst

    global highlow3
    global recLat1
    global recLat2
    global recLat3
    global best1, best2, best3
    global name

    mnths = "12"

    comparefil()

    extension = 'csv'
    all_files = [i for i in glob.glob('police_data*.{}'.format(extension))]

    # combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_files])
    # export to csv
    combined_csv.to_csv("frequencyrec.csv", index=False, encoding='utf-8-sig')

    # first location
    df5 = pd.read_csv("frequencyrec.csv", header=0, escapechar='\\')

    df5.columns = df5.columns.str.strip().str.lower().str.replace(' ', '_')

    newdf = df5[df5['lsoa_name'].str.contains(name)]

    #worst = newdf['lsoa_name'].value_counts()[:5].index.tolist()

    vals = newdf['lsoa_name'].value_counts()

    list = newdf['lsoa_name'].value_counts()[:].sort_values(ascending = False)

    #gets best and worst loactions
    worst1 = str(list.index[0])
    worst2 = str(list.index[1])
    worst3 = str(list.index[2])
    best1 = str(list.index[-1])
    best2 = str(list.index[-2])
    best3 = str(list.index[-3])


    print(vals)
    print(list)
    print(worst1, worst2, worst3)
    print(best1, best2, best3)

    search = worst1 +"|"+ worst2 +"|"+ worst3 +"|"+ best1 +"|"+ best2 +"|"+ best3


    filt = df5.lsoa_name.str.contains(search)


    df6 = df5[filt]

    # get frequencies
    valu = df6["lsoa_name"].value_counts()
    names = df6["lsoa_name"].value_counts().keys()

    list_vals = str(valu)
    count = 0
    highlow3 = ""
    count2=0

    #breaks into a string
    for val in list_vals.split():
        if(count2==6):
            break
        if (count==3):
            highlow3+="<br>"
            if(val=="Name:"):
                break
            else:
                highlow3+=val+" "
                count = 0
                count2+=1
        else:
            highlow3 += val+" "
        count += 1


    # create graph
    plt.title("Crimes per area (Worst 3 vs Best 3)")
    plt.ylabel("Number of crimes committed in last 12 months")
    plt.xlabel("Area")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.rc('font', size=2)

    plt.bar(names, valu)
    plt.savefig('static/IMAGES/recommend/graph3.png', pad_inches=0.1)


    recLatLong(df6)

    os.remove("frequencyrec.csv")

# end of recommendfil()

def recLatLong(df):
    global best1, best2, best3
    global recLat1, recLat2, recLat3
    global recLong1, recLong2, recLong3
    global recLtLn

    search1 = best1
    search2 = best2
    search3 = best3
    print("best1 ", best1)
    filt1 = df.lsoa_name.str.contains(search1)
    filt2 = df.lsoa_name.str.contains(search2)
    filt3 = df.lsoa_name.str.contains(search3)

    df1 = df[filt1]
    df2 = df[filt2]
    df3 = df[filt3]



    rec1 = str(df1[['latitude', 'longitude']].iloc[0])
    rec2 = str(df2[['latitude', 'longitude']].iloc[0])
    rec3 = str(df3[['latitude', 'longitude']].iloc[0])

    rec_list1 = rec1.split()
    recLat1 = rec_list1[rec_list1.index('latitude')+1]
    rec_list2 = rec2.split()
    recLat2 = rec_list2[rec_list2.index('latitude') + 1]
    rec_list3 = rec3.split()
    recLat3 = rec_list3[rec_list3.index('latitude') + 1]

    recLong1 = rec_list1[rec_list1.index('longitude') + 1]

    recLong2 = rec_list2[rec_list2.index('longitude') + 1]

    recLong3 = rec_list3[rec_list3.index('longitude') + 1]

    print(recLat1, recLong1)
    print(recLat2, recLong2)
    print(recLat3, recLong3)

    recLtLn = recLat1+" "+recLong1+" "+recLat2+" "+recLong2+" "+recLat3+" "+recLong3
#end of recLatLong

# !CSV DELETE!
# deletes irrelevant csv columns
def csv_delete():
    f_num = str(file_num)
    print(f_num)
    # pulls specified file from testcsv folder
    file_name = ("crimecsv/" + user_date + "/" + user_date + "-lincolnshire-street.csv")
    # creates new file called 'police_data1', 2, 3... etc
    output_name = 'police_data' + f_num + '.csv'

    # specifies columns to be removed from the file
    cols = [0, 2, 3, 10]

    # reverses the columns so that they are correctly deleted
    cols = sorted(cols, reverse=True)

    rows = 0

    # opens the file and deletes specified column per row
    with open(file_name, "r") as source:
        reader = csv.reader(source)
        with open(output_name, "w", newline='')as result:
            writer = csv.writer(result)
            for row in reader:
                rows += 1
                for col_index in cols:
                    del row[col_index]
                writer.writerow(row)
# end of csv_delete



# prevents other scripts from running
if __name__ == "__main__":
    # runs the app
    app.run(debug=True)