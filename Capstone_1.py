#Import the necessary libraries

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

#Import the necessary CSV files

data = pd.read_csv('C:\Users\RedneckRandy\Documents\GitHub\Capstone-Project-1\GSAF5.xls.csv')


#Clean the CSV data


# Capitalize all columns
data.columns = [col.capitalize().strip() for col in data.columns]

# Remove extra space in column names
data.columns = data.columns.str.replace(' ', '')

# Remove columns starting with "Unnamed"
data = data.loc[:, ~data.columns.str.startswith('Unnamed')]


# Save the cleaned CSV as 'shark_sorted'
data.to_csv('sharks_sorted.csv', index=False)


#Analyze the data

# Count total 'Y' in 'Fatal (Y/N)'
total_Y_fatal = data['Fatal(Y/N)'].str.count('Y').sum()

# Count total 'N' in 'Fatal (Y/N)'
total_N_fatal = data['Fatal(Y/N)'].str.count('N').sum()

# Average 'Age' of total 'Y'
average_age_Y_fatal = data.loc[data['Fatal(Y/N)'] == 'Y', 'Age'].mean()

# Total count for each unique value in 'Location' column
location_totals = data['Location'].value_counts()

# Total count for each unique value in 'Species' column
species_totals = data['Species'].value_counts()

# Total count for each unique value in 'Activity' column
activity_totals = data['Activity'].value_counts()

# Total count for each unique value in 'Type' column
type_totals = data['Type'].value_counts()

# Average of "Time"
time_average = data['Time'].mean()

conn = psycopg2.connect(dbname='gblqlzwo',
                        user='gblqlzwo',
                        password='UkEdnFRHD1w6hKODlEDEqHMIKujC814K',
                        host='rajje.db.elephantsql.com')
cur = conn.cursor()

# Define the columns for the table
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