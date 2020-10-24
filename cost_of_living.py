#import dependencies
import pandas as pd

#Data Scource URL
url = 'https://www.numbeo.com/cost-of-living/rankings.jsp'

#Created a Table into Data Scource
tables = pd.read_html(url)

#Column Names for Data Frame
df = pd.DataFrame(tables[1])
df.columns = ['Rank', 'City', 'COL Index', 'Rent Index', 'COL Plus Rent Index', 
              'Groceries Index', 'Restaurant Price Index', 'Local Purchasing Power Index']

#Separating the the city name from state/country
city_df = df['City'].apply(lambda x: pd.Series(x.split(',')))

#Added the Split_City column into the data frame
df["split_city"] = city_df[0]

#Removed the Rank and COL Plus Rent Index column from the data frame
clean_df = df.drop(['Rank', 'COL Plus Rent Index'], axis=1)

#created the data diction from the data frame
COL_dict = clean_df.to_dict("records")