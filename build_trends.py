
import pandas as pd
from collections import Counter

def build_trend(df):
    trend = {}
    for date in df['date'].unique():
        daily = df[df['date'] == date]['topic']
        trend[date] = Counter(daily)
    return pd.DataFrame(trend).fillna(0).astype(int)
