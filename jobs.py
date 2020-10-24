import requests
import json
import pprint
import pandas as pd

# ---Github Jobs API Call------------------------------------
#endpoont parameters
description = "data science"
location = "usa"
full_time = "true"

#construct endpoint url
url = f"https://jobs.github.com/positions.json?description={description}&full_time={full_time}&location={location}"

#run request and store json response as variable "postings"
postings = requests.get(url).json()

#convert json response into pandas dataframe:
df = pd.DataFrame(postings)
#-----------------------------------------------------------

# ---Data Cleanup---------------------------------------------
# Split Location into City and State Columns
#create dataframe that splits the location string using comma as the delineator
location_df = df['location'].apply(lambda x: pd.Series(x.split(',')))
#add columns for city and state to the main dataframe, using the values in the above dataframe
df["split_city"] = location_df[0]
df["split_state"] = location_df[1]

# Clean up the creation time to just show the date
#create dataframe that splits the created_at string using space as the delineator
created_df = df['created_at'].apply(lambda x: pd.Series(x.split(' ')))
#add column for creation date to the main dataframe, using the month and day values in the above dataframe
df["creation_date"] = created_df[1] + " " + created_df[2]

## Remove html tags from job description
#imported code from internet for a function that will strip html tags from a string
#=============================================
from html.parser import HTMLParser
from io import StringIO

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
#=============================================
#loop through the dataframe rows and run the description through the strip_tags function
#also replace any \n's with blank spaces
for index, row in df.iterrows():
    row["description"] = strip_tags(row["description"])
    row["description"] = row["description"].replace("\n"," ")

# Create list of cities (and remove duplicates) to be used for weather query
cities_list = df["split_city"].to_list()
cities_list = list(dict.fromkeys(cities_list))

# Create clean dataframe of desired data
clean_df = df[["creation_date","title","company","location","split_city","description","url"]]
#---------------------------------------------------------------------------

# ---Data Storing-----------------------------------------------------------
## Convert data into mongo friendly dictionary
postings_dict = clean_df.to_dict("records")
