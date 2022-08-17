import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({'Message':message,'Dates':dates})
    df['Dates'] = pd.to_datetime(df['Dates'], format='%m/%d/%y, %H:%M - ') 

    users = []
    messages = []

    for msg in df['Message']:
        entry = re.split('([\w\w]+?):\s',msg)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("Group Notification")
            messages.append(entry[0])
            
    df['Users'] = users
    df['Messages'] = messages
    df.drop(columns=['Message'],inplace=True)

    df['Only Date'] = df['Dates'].dt.date
    df['Year'] = df['Dates'].dt.year
    df['Month Num'] = df["Dates"].dt.month
    df['Month'] = df['Dates'].dt.month_name()
    df['Day'] = df['Dates'].dt.day
    df['Day Name'] = df['Dates'].dt.day_name()
    df['Hour'] = df['Dates'].dt.hour
    df['Minute'] = df['Dates'].dt.minute
    
    period = []
    for hour in df[['Day Name','Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1)) 
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['Period'] = period

    return df