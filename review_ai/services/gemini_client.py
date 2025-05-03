from google.generativeai import configure, GenerativeModel
from ..config import GEMINI_API_KEY
from typing import List, Dict
import json

class GeminiClient:
    def __init__(self):
        configure(api_key=GEMINI_API_KEY)
        
    def calculate_urgency(self, sentiment: str, confidence: float, themes: List[str], star_rating: int) -> float:
        """Calculate urgency score based on multiple factors"""
        base_score = 0.0
        
        # Negative sentiment with high confidence is urgent
        if sentiment == "Negative" and confidence > 0.7:
            base_score += 0.4
        
        # Low star ratings increase urgency
        if star_rating <= 2:
            base_score += 0.3
        
        # Certain themes indicate higher urgency
        urgent_themes = {"product quality": 0.2, "customer service": 0.15, "shipping speed": 0.1}
        for theme in themes:
            if theme in urgent_themes:
                base_score += urgent_themes[theme]
        
        # Cap at 1.0
        return min(base_score, 1.0)
        
    async def analyze_review(self, review_text: str, star_rating: int) -> dict:
        # Very simple prompt focused on JSON structure
        prompt = (
            'Return ONLY a JSON object like this example, but analyzing this review:\n'
            '{"sentiment":"Positive","confidence_score":0.9,"themes":["product quality"],"response":"Thank you!"}\n\n'
            'Rules:\n'
            '1. sentiment must be: "Positive", "Neutral", or "Negative"\n'
            '2. confidence_score must be: 0.0 to 1.0\n'
            '3. themes must be 1-3 from: ["product quality", "shipping speed", "customer service", "price", "ease of use"]\n'
            '4. response must be: brief and empathetic\n\n'
            f'Review to analyze (rated {star_rating}/5):\n'
            f'"{review_text}"'
        )

        # Using Gemini 2.0 Flash for faster, more efficient processing
        model = GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        
        try:
            # Get raw response
            raw_response = response.text.strip()
            
            # Default response in case of errors
            default_response = {
                "sentiment": "Neutral",
                "confidence_score": 0.5,
                "themes": ["unclear"],
                "response": "Thank you for your review. We'll have our team look into this."
            }
            
            if not raw_response:
                return default_response
                
            # Try to find a JSON object in the response
            import re
            json_match = re.search(r'\{.*?\}', raw_response, re.DOTALL)
            if not json_match:
                return default_response
                
            try:
                # Parse the JSON
                result = json.loads(json_match.group(0))
                
                # Validate fields
                if not isinstance(result, dict) or not all(k in result for k in ['sentiment', 'confidence_score', 'themes', 'response']):
                    return default_response
                    
                # Validate sentiment
                valid_sentiments = ['Positive', 'Neutral', 'Negative']
                if result['sentiment'] not in valid_sentiments:
                    result['sentiment'] = 'Neutral'
                    
                # Validate confidence score
                try:
                    result['confidence_score'] = max(0.0, min(1.0, float(result['confidence_score'])))
                except (ValueError, TypeError):
                    result['confidence_score'] = 0.5
                    
                # Validate themes
                valid_themes = ['product quality', 'shipping speed', 'customer service', 'price', 'ease of use']
                if not isinstance(result['themes'], list):
                    result['themes'] = ['unclear']
                else:
                    result['themes'] = [t for t in result['themes'] if t in valid_themes][:3]
                    if not result['themes']:
                        result['themes'] = ['unclear']
                        
                # Ensure response is a string
                if not isinstance(result['response'], str):
                    result['response'] = default_response['response']
                    
                return result
                
            except json.JSONDecodeError:
                return default_response
                
        except Exception as e:
            print(f"Error processing review: {str(e)}")
            return default_response
