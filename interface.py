import streamlit as st
import re
import pandas as pd
from datetime import datetime
from urlextract import URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import emoji
import seaborn as sns

extract = URLExtract()

def convert_to_24hr_format(date_str, time_str, meridian):
    dt_str = f"{date_str} {time_str} {meridian}"
    dt = datetime.strptime(dt_str, '%m/%d/%y %I:%M %p')
    return dt

dates = []
users = []
messages = []

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])
    
    return emoji_df

def most_common_words(selected_user, df):
    with open(r'D:\vit\ml\whatsapp_chat_analyzer\stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    
    return_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return return_df

def create_wordcloud(selected_user, df):
    with open(r'D:\vit\ml\whatsapp_chat_analyzer\stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df


def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year' , 'month']).count()['message'].reset_index()
    month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    

    # Replace 'month' column with 'month_num'   
    timeline.rename(columns={'month': 'month_num'}, inplace=True)

    # Add new 'month' column with month names
    timeline['month'] = timeline['month_num'].map(month_names)
    
    
    time = []

    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user , df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
    
    
def week_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    return df['day_name'].value_counts()

def month_activity_map(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    return df.pivot_table(index = "day_name" , columns = "period" , values = "message" , aggfunc = "count").fillna(0)

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

st.sidebar.title("WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2})\s?([APMapm]{2})? - (.*?): (.*)'
    
    for match in re.finditer(pattern, data):
        date_str, time_str, meridian, sender, message = match.groups()
        if meridian:
            dt = convert_to_24hr_format(date_str, time_str, meridian)
        else:
            dt = datetime.strptime(f"{date_str} {time_str}", '%m/%d/%y %H:%M')
        dates.append(dt)
        users.append(sender)
        messages.append(message)

    df = pd.DataFrame({'date': dates, 'user': users, 'message': messages})

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    month_names = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    df['month_name'] = df['month'].map(month_names)
    
    period = []
    
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour)+"-"+str('00'))
        elif hour ==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['period'] = period

    # st.dataframe(df)
    
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
            
         #timeline
        
        st.title("Montly Timeline")
        timeline = monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        st.pyplot(fig)
        
        # daily timeline
        
        st.title("Daily Timeline")
        timeline = daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        plt.figure(figsize = (18,10))
        plt.xticks(rotation = 'vertical')
        ax.plot(timeline['only_date'],timeline['message'])
        # ax.plot(timeline['time'],timeline['message'])
        st.pyplot(fig)


        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day = week_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = month_activity_map(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            st.pyplot(fig)
        
        st.title("Weekly activity map")    
        activity = activity_heatmap(selected_user,df)
        fig , ax = plt.subplots()
        ax = sns.heatmap(activity)
        st.pyplot(fig)
        
        
        
        # Busiest User
        if selected_user == 'Overall':
            st.title("Most Busy User")
            col1, col2 = st.columns(2)

            x, new_df = most_busy_users(df)
            fig, ax = plt.subplots()

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        st.title("Wordcloud")       
        df_wc = create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        st.title("Most Common Used Words")
        most_common_df = most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df['word'], most_common_df['count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)

        # Emojis
        st.title("Emoji Analysis")
        emoji_df = emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['count'].head(12), labels=emoji_df['emoji'].head(12), autopct='%0.2f%%')
            st.pyplot(fig)
            
       
