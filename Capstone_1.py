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
columns = ['index', 'Case Number', 'Date', 'Year', 'Type', 'Country', 'Area', 'Location', 'Activity', 'Name',
           'Unnamed: 9', 'Age', 'Injury', 'Fatal (Y/N)', 'Time', 'Species', 'Investigator or Source', 'pdf',
           'href formula', 'href', 'Case Number.1', 'Case Number.2', 'original order']

create_table_query = '''
    CREATE TABLE shark_data(
        "index" INT,
        "Case Number" VARCHAR(100),
        "Date" VARCHAR(100),
        "Year" INT,
        "Type" VARCHAR(100),
        "Country" VARCHAR(100),
        "Area" VARCHAR(100),
        "Location" VARCHAR(100),
        "Activity" VARCHAR(100),
        "Name" VARCHAR(100),
        "Unnamed: 9" VARCHAR(100),
        "Age" VARCHAR(100),
        "Injury" VARCHAR(100),
        "Fatal (Y/N)" VARCHAR(100),
        "Time" VARCHAR(100),
        "Species" VARCHAR(100),
        "Investigator or Source" VARCHAR(100),
        "pdf" VARCHAR(100),
        "href formula" VARCHAR(100),
        "href" VARCHAR(100),
        "Case Number.1" VARCHAR(100),
        "Case Number.2" VARCHAR(100),
        "original order" INT
    )
'''
cur.execute(create_table_query)

for _, row in data[columns].iterrows():
    insert_query = '''
        INSERT INTO shark_data ("Index", "Case Number", "Date", "Year", "Type", "Country", "Area", "Location",
                                 "Activity", "Name", "Age", "Injury", "Fatal(Y/N)", "Time", "Species",
                                 "Investigator or Source", "Pdf", "Href formula", "Href", "Case Number.1",
                                 "Case Number.2", "Original order")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''
    cur.execute(insert_query, tuple(row))

conn.commit()

#Plot the data

plt.figure(figsize=(10, 6))
plt.scatter(data['Species'], data['Type'])
plt.xlabel('Species')
plt.ylabel('Type')
plt.title('Species vs Type')
plt.xticks(rotation=90)
plt.show()

plt.figure(figsize=(10, 6))
plt.scatter(data['Type'], data['Activity'])
plt.xlabel('Type')
plt.ylabel('Activity')
plt.title('Type vs Activity')
plt.xticks(rotation=90)
plt.show()

fatal_counts = data['Fatal (Y/N)'].value_counts()
plt.figure(figsize=(6, 6))
plt.bar(['Y', 'N'], fatal_counts)
plt.xlabel('Fatal')
plt.ylabel('Count')
plt.title('Fatal (Y/N) Distribution')
plt.show()

species_fatal_counts = data.groupby('Species')['Fatal (Y/N)'].value_counts().unstack().fillna(0)
plt.figure(figsize=(10, 6))
species_fatal_counts.plot(kind='bar', stacked=True)
plt.xlabel('Species')
plt.ylabel('Count')
plt.title('Species vs Fatal (Y/N)')
plt.xticks(rotation=90)
plt.legend(title='Fatal (Y/N)')
plt.show()

cur.close()
conn.close()