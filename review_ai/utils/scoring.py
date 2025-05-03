def calculate_urgency_score(review_data: dict) -> float:
    """
    Calculate urgency score based on:
    - Sentiment (negative sentiment needs more urgent attention)
    - Star rating (lower ratings need more urgent attention)
    - Keywords indicating urgency
    
    Returns a score between 0 and 1, where 1 is most urgent
    """
    score = 0.0
    
    # Sentiment-based scoring
    if review_data["sentiment"].lower() == "negative":
        score += 0.4
    elif review_data["sentiment"].lower() == "neutral":
        score += 0.2
    
    # Star rating-based scoring (if available)
    if "star_rating" in review_data:
        score += (5 - review_data["star_rating"]) * 0.1
    
    # Keyword-based scoring
    urgent_keywords = ["urgent", "immediately", "asap", "broken", "defective", 
                      "refund", "return", "damaged", "safety", "dangerous"]
    
    review_text = review_data.get("review_text", "").lower()
    for keyword in urgent_keywords:
        if keyword in review_text:
            score += 0.1
            break
    
    return min(1.0, score)  # Cap at 1.0
