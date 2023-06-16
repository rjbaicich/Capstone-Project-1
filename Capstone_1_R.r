#Install necessary packages and libraries.

install.packages("ggplot2")
install.packages("tidyverse")
install.packages("tidyr")

library(ggplot2)
library(tidyverse)
library(tidyr)

# Import the CSV file
data <- read.csv("C:\Users\RedneckRandy\Documents\GitHub\Capstone-Project-1\GSAF5.xls.csv")

# Remove columns starting with "Unnamed"
data <- data[, !grepl("^Unnamed", names(data))]

# Remove extra space in column names
names(data) <- gsub("\\s+", "", names(data))

# Capitalize all columns
names(data) <- toupper(names(data))

# Percent of 'Y' vs Percent of 'N' in "Fatal (Y/N)" column
percent_Y <- sum(data$FATALYN == "Y") / nrow(data) * 100
percent_N <- sum(data$FATALYN == "N") / nrow(data) * 100

# Percent of each unique value in "Location" column
location_percent <- prop.table(table(data$LOCATION)) * 100

# Percent of each unique value in "Injury" column
injury_percent <- prop.table(table(data$INJURY)) * 100

# Average of "Time"
time_average <- mean(data$TIME)

# Graph 1: "Injury" vs "Fatal (Y/N)"
library(ggplot2)
ggplot(data, aes(x = INJURY, fill = FATALYN)) +
  geom_bar() +
  labs(x = "Injury", y = "Count", title = "Injury vs Fatal (Y/N)")

# Graph 2: "Location" vs "Time"
ggplot(data, aes(x = LOCATION, y = TIME)) +
  geom_point() +
  labs(x = "Location", y = "Time", title = "Location vs Time")
