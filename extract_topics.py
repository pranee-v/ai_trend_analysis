
def extract_topics(review):
    review = review.lower()
    topics = []
    if "rude" in review or "behaved badly" in review:
        topics.append("Delivery partner rude")
    if "late" in review:
        topics.append("Late delivery")
    if "stale" in review:
        topics.append("Food stale")
    if "crash" in review:
        topics.append("App crash")
    return topics
