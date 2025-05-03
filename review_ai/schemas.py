from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class ReviewRequest(BaseModel):
    review_text: str
    product_category: str
    star_rating: int
    date_submitted: datetime

class ReviewAnalysis(BaseModel):
    sentiment: str = Field(..., description="Positive, Neutral, or Negative")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    themes: List[str] = Field(..., description="List of themes found in the review")
    response: str = Field(..., description="Generated response template")
    urgency_score: float = Field(..., ge=0.0, le=1.0, description="Score indicating review urgency")
    product_category: str = Field(..., description="Product category of the review")
    
class DashboardMetrics(BaseModel):
    sentiment_distribution: Dict[str, int] = Field(default_factory=dict)
    common_themes: Dict[str, int] = Field(default_factory=dict)
    urgent_reviews: List[ReviewAnalysis] = Field(default_factory=list)
    category_sentiment: Dict[str, Dict[str, int]] = Field(default_factory=dict)
    metrics: Dict[str, float] = Field(default_factory=dict)
