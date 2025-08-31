"""
Required Args

['id', 'Podcast_Name', 'Episode_Title', 'Episode_Length_minutes',
       'Genre', 'Host_Popularity_percentage', 'Publication_Day',
       'Publication_Time', 'Guest_Popularity_percentage', 'Number_of_Ads',
       'Episode_Sentiment', 'Listening_Time_minutes']

['Podcast_Name', 'Episode_Title', 'Episode_Length_minutes', 'Genre',
       'Host_Popularity_percentage', 'Publication_Day', 'Publication_Time',
       'Guest_Popularity_percentage', 'Number_of_Ads', 'Episode_Sentiment',
       'Listening_Time_minutes']

cat_clos:

['Pub_DateTime', 'Publication_Day', 'Episode_Sentiment', 'Episode_Title', 'Number_of_Ads', 'GuestPop_Int', 'Publication_Time', 'Genre', 'GuestPop_Dec', 'Podcast_Name']
"""

import os
import numpy as np
import pandas as pd
from joblib import load

from src.inference.settings import MODEL_DIR


# def make_ftre(data) -> pd.DataFrame:
#     # Combine publication day and time into a single datetime-like feature
#     pub_datetime = f"{data.pub_day}-{data.pub_day_time}"

#     # Clip the number of ads between 0 and 3
#     num_ads = min(max(data.nums_of_ads, 0), 3)

#     # Breakdown guest popularity into int and decimal
#     guest_pop_int = int(np.floor(data.guest_popu_percentage))
#     guest_pop_dec = data.guest_popu_percentage - guest_pop_int

#     # Compute engineered features
#     total_pop = data.guest_popu_percentage + data.host_popu_percentage
#     diff_pop = data.guest_popu_percentage - data.host_popu_percentage
#     totalpop_vs_ads = np.log1p(total_pop) - np.log1p(num_ads)

#     return pd.DataFrame([{
#         "Pub_DateTime": pub_datetime,
#         "Publication_Day": data.pub_day,
#         "Publication_Time": data.pub_day_time,
#         "Genre": data.genre,
#         "Podcast_Name": data.podcast_name,
#         "Episode_Title": data.episode_title,
#         "Episode_Sentiment": data.episode_sentiment,
#         "Episode_Length_minutes": data.episode_length,
#         "Number_of_Ads": np.uint8(num_ads),
#         "Guest_Popularity_percentage": data.guest_popu_percentage,
#         "Host_Popularity_percentage": data.host_popu_percentage,
#         "GuestPop_Int": np.int16(guest_pop_int),
#         "GuestPop_Dec": guest_pop_dec,
#         "Total_Pop": total_pop,
#         "Diff_Pop": diff_pop,
#         "TotalPop_vs_Ads": totalpop_vs_ads,
#     }])


def make_ftre(data) -> pd.DataFrame:
    # Create combined datetime-like feature
    pub_datetime = f"{data['pub_day']}-{data['pub_day_time']}"

    # Clamp ads between 0 and 3
    num_ads = min(max(data['nums_of_ads'], 0), 8)

    # Guest popularity parts
    guest_pop_int = int(np.floor(data['guest_popu_percentage']))
    guest_pop_dec = data['guest_popu_percentage'] - guest_pop_int

    # Engineered features
    total_pop = data['guest_popu_percentage'] + data['host_popu_percentage']
    diff_pop = data['guest_popu_percentage'] - data['host_popu_percentage']
    totalpop_vs_ads = np.log1p(total_pop) - np.log1p(num_ads)

    return pd.DataFrame(
        [
            {
                # Categorical features
                "Pub_DateTime": pub_datetime,
                "Publication_Day": data['pub_day'],
                "Episode_Sentiment": data['episode_sentiment'],
                "Episode_Title": data['episode_title'],
                "Number_of_Ads": str(int(num_ads)),  # Cast to string
                "GuestPop_Int": str(guest_pop_int),  # Cast to string
                "GuestPop_Dec": str(round(guest_pop_dec, 3)),  # Cast to string
                "Publication_Time": data['pub_day_time'],
                "Genre": data['genre'],
                "Podcast_Name": data['podcast_name'],
                # Numerical (continuous) features
                "Guest_Popularity_percentage": data['guest_popu_percentage'],
                "Host_Popularity_percentage": data['host_popu_percentage'],
                "Episode_Length_minutes": data['episode_length'],
                "Total_Pop": total_pop,
                "Diff_Pop": diff_pop,
                "TotalPop_vs_Ads": totalpop_vs_ads,
            }
        ]
    )


def load_models():
    models = []
    for filename in os.listdir(MODEL_DIR):
        if filename.endswith(".pkl"):
            model_path = os.path.join(MODEL_DIR, filename)
            model = load(model_path)
            models.append(model)
    return models
