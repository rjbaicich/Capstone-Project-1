
#Load required libraries
library(dplyr)
library(ggplot2)

#Set the file path
file_path <- "C:/Users/RedneckRandy/Downloads/archive (15)/GSAF5.csv"

#Import the CSV file
data <- read.csv(file_path, stringsAsFactors = FALSE)

#Clean the CSV file
cleaned_data <- data %>%
  select(-matches("^(u|U)nnamed")) %>%
  na.omit()
print(cleaned_data)

#Calculate the number of occurrences for each species
species_occurrences <- cleaned_data %>%
  group_by(`Species`) %>%
  summarize(Count = n()) %>%
  arrange(desc(Count))
print(species_occurrences)

#Convert "Time" column to numeric
cleaned_data$Time <- as.numeric(as.character(cleaned_data$Time))

#Calculate the average of "Time"
average_time <- cleaned_data %>%
  summarize(Average_Time = mean(Time, na.rm = TRUE))

#Print the average time
print(average_time)

#Get the top 10 locations based on occurrence count
top_locations <- cleaned_data %>%
  group_by(Location) %>%
  summarize(Count = n()) %>%
  arrange(desc(Count)) %>%
  top_n(10)
print(top_locations)

#Calculate the number of occurrences for each country
country_occurrences <- cleaned_data %>%
  group_by(Country) %>%
  summarize(Count = n()) %>%
  arrange(desc(Count))
print(country_occurrences)

#Calculate the number of occurrences for each activity
activity_occurrences <- cleaned_data %>%
  group_by(Activity) %>%
  summarize(Count = n()) %>%
  arrange(desc(Count))
print(activity_occurrences)

#Filter the cleaned_data to include only the top 10 locations
filtered_data <- cleaned_data %>%
  filter(Location %in% top_locations$Location)

#Calculate the average age for each location
avg_age <- filtered_data %>%
  group_by(Location) %>%
  summarize(Average_Age = mean(Age, na.rm = TRUE)) %>%
  arrange(desc(Average_Age)) %>%
  top_n(10)

#Graph: Top 10 Locations vs Average Age
graph <- ggplot(avg_age, aes(x = reorder(Location, Average_Age), y = Average_Age)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(x = "Location", y = "Average Age") +
  ggtitle("Top 10 Locations vs Average Age") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

#Graph 2: Top 10 Countries vs Number of Occurrences
top_10_countries <- head(country_occurrences, 10)  #Select the top 10 countries

graph3 <- ggplot(top_10_countries, aes(x = Country, y = Count)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(x = "Country", y = "Number of Occurrences") +
  ggtitle("Number of Occurrences by Country (Top 10)") +
  theme_bw() +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

print(graph3)

#Print the analysis results
print(average_time)

print(species_occurrences)

print(country_occurrences)

print(activity_occurrences)

print(top_locations)