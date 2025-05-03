from .gemini_client import GeminiClient
from ..utils.scoring import calculate_urgency_score
from ..schemas import ReviewRequest

class ReviewEngine:
    def __init__(self):
        self.gemini_client = GeminiClient()
    
    async def process_review(self, review_request: ReviewRequest) -> dict:
        """Process a customer review using the Gemini API and calculate urgency score"""
        # Get AI analysis with star rating context
        result = await self.gemini_client.analyze_review(
            review_text=review_request.review_text,
            star_rating=review_request.star_rating
        )
        
        # Calculate urgency score
        result['urgency_score'] = self.gemini_client.calculate_urgency(
            sentiment=result['sentiment'],
            confidence=result['confidence_score'],
            themes=result['themes'],
            star_rating=review_request.star_rating
        )
        
        # Add metadata for tracking and dashboard
        result['product_category'] = review_request.product_category
        result['review_id'] = review_request.review_id
        
        return result
