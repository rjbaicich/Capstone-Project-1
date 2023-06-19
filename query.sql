# Query 1: Retrieve all rows from the "shark_data" table
select_query = "SELECT * FROM shark_data"

# Query 2: Get the total count of shark attacks by year
SELECT "Year", 
COUNT(*) AS "TotalAttacks" 
FROM shark_data 
GROUP BY "Year" 
ORDER BY "Year";

# Query 3: Find the top 5 countries with the highest number of shark attacks
SELECT "Country",
COUNT(*) AS "TotalAttacks"
FROM shark_data
GROUP BY "Country"
ORDER BY "TotalAttacks"
DESC LIMIT 5;
