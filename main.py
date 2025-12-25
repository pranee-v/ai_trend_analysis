import os
import pandas as pd
from datetime import datetime, timedelta
from extract_topics import extract_topics
import random


app_link = input("https://play.google.com/store/apps/details?id=com.swiggy.delivery")

start_date = datetime(2025, 11, 25)
end_date = datetime(2025, 12, 25)  # You can change to datetime.now()
num_reviews_per_day = 5

print(f"Generating synthetic reviews for app: {app_link}")

sample_reviews = [
    "Delivery was late",
    "Food was cold",
    "App crashed during ordering",
    "Payment failed",
    "Delivery guy was rude",
    "Maps not working properly",
    "Offers not applied",
    "Order missing items",
    "Customer support was helpful",
    "Great food, fast delivery"
]

reviews = []
current_date = start_date
while current_date <= end_date:
    for _ in range(num_reviews_per_day):
        review_text = random.choice(sample_reviews)
        reviews.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "review": review_text
        })
    current_date += timedelta(days=1)

os.makedirs("data", exist_ok=True)
df = pd.DataFrame(reviews)
df.to_csv("data/reviews.csv", index=False)
print(f"{len(df)} synthetic reviews saved to data/reviews.csv")

df['date'] = pd.to_datetime(df['date'])
all_dates = pd.date_range(end_date - timedelta(days=29), end_date)

rows = []
for _, r in df.iterrows():
    topics = extract_topics(r['review'])
    for t in topics:
        rows.append({"date": r['date'], "topic": t})

topic_df = pd.DataFrame(rows)
unique_topics = topic_df['topic'].unique() if not topic_df.empty else []
trend_df = pd.DataFrame(0, index=unique_topics, columns=all_dates)

for date in all_dates:
    daily_counts = topic_df[topic_df['date'] == date]['topic'].value_counts()
    for topic, count in daily_counts.items():
        trend_df.loc[topic, date] = count

trend_df.columns = [d.strftime('%b %d') for d in trend_df.columns]

os.makedirs("output", exist_ok=True)
output_path = "output/trend_report.csv"
trend_df.index.name = "Topic"
trend_df.reset_index().to_csv(output_path, index=False)
print("Trend report generated in output/trend_report.csv")
