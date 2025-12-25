import os
import pandas as pd
from collections import Counter
from datetime import timedelta

# ---------- SIMPLIFIED TOPIC EXTRACTION ----------
# Replace this with LLM or agent logic if desired
def extract_topics(review):
    review = review.lower()
    topics = []
    if "rude" in review or "behaved badly" in review:
        topics.append("Delivery partner rude")
    if "late" in review or "delay" in review:
        topics.append("Delivery issue")
    if "stale" in review or "cold" in review:
        topics.append("Food stale")
    if "maps" in review or "location" in review:
        topics.append("Maps not working properly")
    if "instamart" in review or "open all night" in review:
        topics.append("Instamart should be open all night")
    if "10 minute" in review or "bolt delivery" in review:
        topics.append("Bring back 10 minute bolt delivery")
    if "crash" in review or "app closed" in review:
        topics.append("App crash")
    # Add more rules if needed
    return topics

# ---------- MAIN PIPELINE ----------
os.makedirs("output", exist_ok=True)

# Load reviews CSV
df = pd.read_csv("data/reviews.csv")
df['date'] = pd.to_datetime(df['date'])

# Determine target date T (latest date in CSV)
T = df['date'].max()
T_30 = T - timedelta(days=29)  # last 30 days
all_dates = pd.date_range(T_30, T)

# Extract topics for each review
rows = []
for _, r in df.iterrows():
    if r['date'] < T_30:  # ignore reviews older than T-30
        continue
    topics = extract_topics(r['review'])
    for t in topics:
        rows.append({"date": r['date'], "topic": t})

topic_df = pd.DataFrame(rows)

# Build empty trend table with topics as rows and 30 days as columns
unique_topics = topic_df['topic'].unique() if not topic_df.empty else []
trend_df = pd.DataFrame(0, index=unique_topics, columns=all_dates)

# Fill in counts
for date in all_dates:
    daily_counts = topic_df[topic_df['date'] == date]['topic'].value_counts()
    for topic, count in daily_counts.items():
        trend_df.loc[topic, date] = count

# Format columns as readable dates (e.g., Jun 01)
trend_df.columns = [d.strftime('%b %d') for d in trend_df.columns]

# Reset index and save CSV
trend_df.index.name = "Topic"
trend_df.reset_index().to_csv("output/trend_report.csv", index=False)

print("Trend report generated in output/trend_report.csv")
