# WhatsApp Chat Analyzer

## Introduction
This project is a Streamlit-based application that allows users to analyze WhatsApp chat data. The analyzer provides insights such as the most active users, commonly used words, shared media, links, and emoji usage. It also visualizes activity trends over time with various charts and graphs.

## Features
- **Upload WhatsApp Chat File:** Upload your WhatsApp chat text file to the application.
- **Top Statistics:** Displays total messages, total words, media shared, and links shared.
- **Monthly and Daily Timeline:** Visualizes chat activity over months and days.
- **Activity Map:** Shows the most busy days and months.
- **Weekly Activity Map:** Heatmap visualization of weekly activity.
- **Most Busy Users:** Identifies the most active users in the chat.
- **Wordcloud:** Generates a word cloud of the most frequently used words.
- **Most Common Words:** Displays the most commonly used words excluding stop words.
- **Emoji Analysis:** Analyzes and visualizes the most used emojis.
## Requirements
Make sure you have the following packages installed:

- streamlit
- pandas
- datetime
- urlextract
- matplotlib
- wordcloud
- collections
- emoji
- seaborn

## Functions
### Data Processing
- **convert_to_24hr_format:** Converts 12-hour time format to 24-hour format.
- **emoji_helper:** Analyzes and counts emojis used in the chat.
- **most_common_words:** Identifies the most common words used in the chat.
- **create_wordcloud:** Generates a word cloud from the chat messages.
- **most_busy_users:** Identifies the most active users in the chat.
- **monthly_timeline:** Generates a monthly timeline of message counts.
- **daily_timeline:** Generates a daily timeline of message counts.
- **week_activity_map:** Maps activity by day of the week.
- **month_activity_map:** Maps activity by month.
- **activity_heatmap:** Creates a heatmap of activity by day and period.
- **fetch_stats:** Fetches basic statistics about the chat.
