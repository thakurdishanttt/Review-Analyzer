from fastapi import FastAPI, HTTPException, UploadFile, File
from .schemas import ReviewRequest, ReviewAnalysis, DashboardMetrics
from .services.review_engine import ReviewEngine
from typing import List, Dict
from datetime import datetime
import json

app = FastAPI()
review_engine = ReviewEngine()

# In-memory store for reviews
reviews_store: List[ReviewAnalysis] = []

@app.post("/analyze/upload-json")
async def upload_reviews_json(file: UploadFile = File(...)):
    try:
        content = await file.read()
        reviews_data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
    
    if not isinstance(reviews_data, list):
        reviews_data = [reviews_data]
    
    if not reviews_data:
        raise HTTPException(status_code=400, detail="No reviews found in file")
    
    results = []
    for review_data in reviews_data:
        try:
            # Convert the review data to a ReviewRequest object
            # If review_id is not provided, it will be auto-generated
            review_request = ReviewRequest(
                review_text=review_data["review_text"],
                product_category=review_data["product_category"],
                star_rating=review_data["star_rating"],
                date_submitted=datetime.strptime(review_data["date_submitted"], "%Y-%m-%d")
            )
            
            # Process the review
            result = await review_engine.process_review(review_request)
            analysis = ReviewAnalysis(**result)
            
            # Store for dashboard
            reviews_store.append(analysis)
            results.append(analysis)
            
        except Exception as e:
            # Log the error but continue processing other reviews
            print(f"Error processing review: {str(e)}")
            continue
    
    if not results:
        raise HTTPException(status_code=500, detail="Error processing all reviews")
    
    return results

@app.get("/dashboard")
async def get_dashboard():
    if not reviews_store:
        return {
            "sentiment_distribution": {},
            "common_themes": {},
            "urgent_reviews": [],
            "metrics": {
                "total_reviews": 0,
                "average_confidence": 0,
                "average_urgency": 0,
                "urgent_review_ratio": 0
            }
        }
    
    # Calculate sentiment distribution
    sentiment_dist = {}
    for review in reviews_store:
        sentiment_dist[review.sentiment] = sentiment_dist.get(review.sentiment, 0) + 1
    
    # Find common themes
    theme_counts: Dict[str, int] = {}
    for review in reviews_store:
        for theme in review.themes:
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
    
    # Get urgent reviews (urgency score > 0.7)
    urgent_reviews = [
        {
            "review_id": review.review_id,
            "text": review.response,
            "urgency_score": review.urgency_score,
            "sentiment": review.sentiment
        }
        for review in reviews_store
        if review.urgency_score > 0.7
    ]
    
    # Calculate averages
    for review in reviews_store:
        if hasattr(review, 'product_category'):
            category_sentiment[review.product_category][review.sentiment] += 1
    
    # Calculate evaluation metrics
    total_reviews = len(reviews_store)
    avg_confidence = sum(r.confidence_score for r in reviews_store) / total_reviews if total_reviews > 0 else 0
    avg_urgency = sum(r.urgency_score for r in reviews_store) / total_reviews if total_reviews > 0 else 0
    urgent_ratio = len([r for r in reviews_store if r.urgency_score > 0.7]) / total_reviews if total_reviews > 0 else 0
    
    return DashboardMetrics(
        sentiment_distribution=dict(sentiment_dist),
        common_themes=dict(sorted(themes_count.items(), key=lambda x: x[1], reverse=True)[:10]),
        urgent_reviews=urgent_reviews,
        category_sentiment={k: dict(v) for k, v in category_sentiment.items()},
        metrics={
            "total_reviews": total_reviews,
            "average_confidence": round(avg_confidence, 2),
            "average_urgency": round(avg_urgency, 2),
            "urgent_review_ratio": round(urgent_ratio, 2)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
