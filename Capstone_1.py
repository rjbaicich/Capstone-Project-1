#Import the necessary libraries

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

#Import the necessary CSV files

df = pd.read_csv(r'C:\Users\RedneckRandy\Documents\GitHub\Capstone-Project-1\GSAF5.csv', low_memory=False)


#Clean the CSV data


#Capitalize all columns
df.columns = [col.capitalize().strip() for col in df.columns]

#Remove extra space in column names
df.columns = df.columns.str.replace(' ', '')

#Drop the first column
df = df.drop(df.columns[0], axis=1)

# Remove columns starting with "Unnamed"
df = df.loc[:, ~df.columns.str.startswith('Unnamed')]


#Save the cleaned CSV as 'shark_sorted'
df.to_csv('sharks_sorted.csv', index=False)


#Analyze the data

#Total Count of 'Y' in 'Fatal (Y/N)'
total_Y_fatal = df['Fatal(y/n)'].str.count('Y').sum()

#Total Count of 'N' in 'Fatal (Y/N)'
total_N_fatal = df['Fatal(y/n)'].str.count('N').sum()

#Convert 'Age' column to numeric using .loc
df.loc[:, 'Age'] = pd.to_numeric(df['Age'], errors='coerce')

#Filter the dataframe for records where 'Fatal(y/n)' is 'Y'
df_Y_fatal = df[df['Fatal(y/n)'] == 'Y']

#Calculate the average 'Age' for the filtered dataframe
average_age_Y_fatal = df_Y_fatal['Age'].mean()

#Total count for each unique value in 'Location' column
location_totals = df['Location'].value_counts()

#Total count for each unique value in 'Species' column
species_totals = df['Species'].value_counts()

#Total count for each unique value in 'Activity' column
activity_totals = df['Activity'].value_counts()

#Total count for each unique value in 'Type' column
type_totals = df['Type'].value_counts()

#Convert 'Time' column to numeric using .loc
df.loc[:, 'Time'] = pd.to_numeric(df['Time'], errors='coerce')

#Filter the dataframe for records where 'Fatal(y/n)' is 'Y'
df_Y_fatal = df[df['Fatal(y/n)'] == 'Y']

#Calculate the average 'Age' for the filtered dataframe
average_time_Y_fatal = df_Y_fatal['Time'].mean()

conn = psycopg2.connect(dbname='gblqlzwo',
                        user='gblqlzwo',
                        password='UkEdnFRHD1w6hKODlEDEqHMIKujC814K',
                        host='rajje.db.elephantsql.com')
cur = conn.cursor()

#Define the columns for the table
columns = ['Date', 'Year', 'Type', 'Country', 'Area', 'Location', 'Activity', 'Name', 'Age', 'Injury', 'Fatal(y/n)', 'Time', 'Species']

create_table_query = '''
    CREATE TABLE shark_data(
        "Date" VARCHAR(200),
        "Year" INT,
        "Type" VARCHAR(200),
        "Country" VARCHAR(200),
        "Area" VARCHAR(200),
        "Location" VARCHAR(200),
        "Activity" VARCHAR(200),
        "Name" VARCHAR(200),
        "Age" VARCHAR(200),
        "Injury" VARCHAR(200),
        "Fatal(y/n)" VARCHAR(200),
        "Time" VARCHAR(200),
        "Species" VARCHAR(200)
    )
'''
cur.execute(create_table_query)

for _, row in df[columns].iterrows():
    insert_query = '''
        INSERT INTO shark_data ("Date", "Year", "Type", "Country", "Area", "Location",
                                 "Activity", "Name", "Age", "Injury", "Fatal(y/n)", "Time", "Species")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cur.execute(insert_query, tuple(row))
    
    conn.commit()

#Counting the occurrences of each activity
activity_counts = df['Activity'].value_counts()

#Selecting the top 15 activities
top_activities = activity_counts.head(7)

#Calculating the percentage of each activity
activity_percentages = (top_activities / len(df)) * 100

#Creating the pie chart
plt.figure(figsize=(8, 8))
plt.pie(activity_percentages, labels=activity_percentages.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')  #Equal aspect ratio ensures that pie is drawn as a circle
plt.title('Percentage of Attacks for the Top 7 Activities')
plt.show()

#Extracting the required columns for analysis
countries = df['Country'].dropna()

#Counting the number of shark attacks per country
attacks_per_country = countries.value_counts()[:20]

#Creating the bar chart for shark attacks per country
plt.figure(figsize=(12, 8))
plt.bar(attacks_per_country.index, attacks_per_country.values, color='red')
plt.xlabel('Country')
plt.ylabel('Number of Shark Attacks')
plt.title('Number of Shark Attacks per Country (Top 10)')
plt.xticks(rotation=45)
plt.show()

top_10_species = df[df['Fatal(y/n)'] == 'Y']['Species'].value_counts().nlargest(10)
plt.figure(figsize=(10, 8))
top_10_species.plot(kind='bar')
plt.xlabel('Species')
plt.ylabel('Number of Fatalities')
plt.title('Top 10 Species with the Most Fatalities')    
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

cur.close()
conn.close()