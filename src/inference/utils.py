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
"""

import numpy as np

def make_ftre(data) -> dict:
    pub_datetime = f"{data.pub_day}-{data.pub_day_time}"
    num_ads = min(max(data.nums_of_ads, 0), 3)

    guest_pop_int = int(np.floor(data.guest_popu_percentage))
    guest_pop_dec = data.guest_popu_percentage - guest_pop_int

    total_pop = data.guest_popu_percentage + data.host_popu_percentage
    diff_pop = data.guest_popu_percentage - data.host_popu_percentage

    totalpop_vs_ads = np.log1p(total_pop) - np.log1p(num_ads)

    return {
        "Pub_DateTime": pub_datetime,
        "Number_of_Ads": np.uint8(num_ads),
        "GuestPop_Int": np.int16(guest_pop_int),
        "GuestPop_Dec": guest_pop_dec,
        "Total_Pop": total_pop,
        "Diff_Pop": diff_pop,
        "TotalPop_vs_Ads": totalpop_vs_ads,
    }
