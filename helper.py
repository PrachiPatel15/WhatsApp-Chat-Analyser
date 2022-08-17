from re import U
import pandas as pd
import emoji
from collections import Counter
from urlextract import URLExtract
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user == 'Overall':
        num_messages = df.shape[0]

        words = []
        for msg in df['Messages']:
            words.extend(msg.split())

        media_total = df[df["Messages"] == '<Media omitted>\n'].shape[0]

        links = []
        for msg in df['Messages']:
            links.extend(extract.find_urls(msg))

        return num_messages,len(words),media_total,len(links)

    else:
        new_df = df[df['Users']== selected_user]
        num_messages = new_df.shape[0]
        
        words = []
        for msg in new_df['Messages']:
            words.extend(msg.split())

        media_total = new_df[new_df["Messages"] == '<Media omitted>\n'].shape[0]

        links = []
        for msg in new_df['Messages']:
            links.extend(extract.find_urls(msg))

        return num_messages,len(words),media_total,len(links)

def most_busy_user(df):
    x = df['Users'].value_counts().head()
    percentage = round((df['Users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns=
                                                            {'index':'name','Users':'percentage'})
    return x, percentage  

def most_common_words(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    temp = df[df['Users'] != 'group_notification']
    temp = temp[temp['Messages'] != '<Media omitted>\n']

    words = []
    for msg in temp['Messages']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def analyse_emoji(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    emojis = []
    for msg in df['Messages']:
        emojis.extend([c for c in msg if c in emoji.distinct_emoji_list(c)])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    timeline = df.groupby(['Year','Month Num','Month']).count()['Messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + '-' + str(timeline['Year'][i]))
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    daily_timeline = df.groupby('Only Date').count()['Messages'].reset_index()
    return daily_timeline

def week_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    return df['Day Name'].value_counts()

def month_activity(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    user_heatmap = df.pivot_table(index='Day Name',columns='Period',values='Messages',aggfunc='count').fillna(0)
    return user_heatmap