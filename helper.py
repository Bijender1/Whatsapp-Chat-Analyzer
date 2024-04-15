from collections import Counter

import pandas as pd
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_extra.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stop_extra.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# def emoji_helper(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     emoji_counts = {}
#     for message in df['message']:
#         emojis_in_message = [c for c in message if c in emoji.UNICODE_EMOJI['en']]
#         for emoji_char in emojis_in_message:
#             if emoji_char in emoji_counts:
#                 emoji_counts[emoji_char] += 1
#             else:
#                 emoji_counts[emoji_char] = 1
#
#     emoji_df = pd.DataFrame(list(emoji_counts.items()), columns=['Emoji', 'Count'])
#     emoji_df = emoji_df.sort_values(by='Count', ascending=False)
#
#     return emoji_df

def is_emoji(char):
        emoji_ranges = [
            (0x1F300, 0x1F320), (0x1F330, 0x1F335), (0x1F337, 0x1F37C),
            (0x1F380, 0x1F393), (0x1F3A0, 0x1F3C4), (0x1F3C6, 0x1F3CA),
            (0x1F3E0, 0x1F3F0), (0x1F400, 0x1F43E), (0x1F440, 0x1F440),
            (0x1F442, 0x1F4F7), (0x1F4F9, 0x1F4FC), (0x1F500, 0x1F53C),
            (0x1F540, 0x1F543), (0x1F550, 0x1F567), (0x1F5FB, 0x1F5FF),
            (0x1F600, 0x1F64F), (0x1F680, 0x1F6C5), (0x1F6CC, 0x1F6CC),
            (0x1F90D, 0x1F90D), (0x1F90F, 0x1F90F), (0x1F911, 0x1F917),
            (0x1F920, 0x1F927), (0x1F930, 0x1F930), (0x1F933, 0x1F93E),
            (0x1F940, 0x1F94B), (0x1F950, 0x1F95E), (0x1F980, 0x1F991),
            (0x1F9C0, 0x1F9C0), (0x1F9D0, 0x1F9E6), (0x200D, 0x200D),
            (0x203C, 0x203C), (0x2049, 0x2049), (0x2122, 0x2122),
            (0x2139, 0x2139), (0x2194, 0x2199), (0x21A9, 0x21AA),
            (0x231A, 0x231B), (0x2328, 0x2328), (0x23CF, 0x23CF),
            (0x23E9, 0x23F3), (0x23F8, 0x23FA), (0x24C2, 0x24C2),
            (0x25AA, 0x25AB), (0x25B6, 0x25B6), (0x25C0, 0x25C0),
            (0x25FB, 0x25FE), (0x2600, 0x2604), (0x260E, 0x260E),
            (0x2611, 0x2611), (0x2614, 0x2615), (0x2618, 0x2618),
            (0x261D, 0x261D), (0x2620, 0x2620), (0x2622, 0x2623),
            (0x2626, 0x2626), (0x262A, 0x262A), (0x262E, 0x262F),
            (0x2638, 0x263A), (0x2640, 0x2640), (0x2642, 0x2642),
            (0x2648, 0x2653), (0x2660, 0x2660), (0x2663, 0x2663),
            (0x2665, 0x2666), (0x2668, 0x2668), (0x267B, 0x267B),
            (0x267F, 0x267F), (0x2692, 0x2697), (0x2699, 0x2699),
            (0x269B, 0x269C), (0x26A0, 0x26A1), (0x26AA, 0x26AB),
            (0x26B0, 0x26B1), (0x26BD, 0x26BE), (0x26C4, 0x26C5),
            (0x26C8, 0x26C8), (0x26CE, 0x26CF), (0x26D1, 0x26D1),
            (0x26D3, 0x26D4), (0x26E9, 0x26EA), (0x26F0, 0x26F5),
            (0x26F7, 0x26FA), (0x26FD, 0x26FD), (0x2702, 0x2702),
            (0x2705, 0x2705), (0x2708, 0x2709), (0x270A, 0x270B),
            (0x270C, 0x270D), (0x270F, 0x270F), (0x2712, 0x2712),
            (0x2714, 0x2714), (0x2716, 0x2716), (0x271D, 0x271D),
            (0x2721, 0x2721), (0x2728, 0x2728), (0x2733, 0x2734),
            (0x2744, 0x2744), (0x2747, 0x2747), (0x274C, 0x274C),
            (0x274E, 0x274E), (0x2753, 0x2755), (0x2757, 0x2757),
            (0x2763, 0x2764), (0x2795, 0x2797), (0x27A1, 0x27A1),
            (0x27B0, 0x27B0), (0x27BF, 0x27BF)]
        return any(start <= ord(char) <= end for start, end in emoji_ranges)


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emoji_counts = {}
    for message in df['message']:
        emojis_in_message = [c for c in message if is_emoji(c)]
        for emoji_char in emojis_in_message:
            if emoji_char in emoji_counts:
                emoji_counts[emoji_char] += 1
            else:
                emoji_counts[emoji_char] = 1

    emoji_df = pd.DataFrame(list(emoji_counts.items()), columns=['Emoji', 'Count'])
    emoji_df = emoji_df.sort_values(by='Count', ascending=False)

    emoji_text = ''.join([emoji.emojize(f':{em}:') * count for em, count in emoji_counts.items()])  # Changed 'emoji' to 'em'

    return emoji_df, emoji_text

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap















