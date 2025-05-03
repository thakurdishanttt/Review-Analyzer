# Customer Review Analysis System

A FastAPI application that analyzes customer reviews using Google's Gemini 2.0 Flash API to provide comprehensive review analysis and response generation.

## Features

1. **Sentiment Analysis**
   - Classifies reviews as Positive, Neutral, or Negative
   - Provides confidence scores for sentiment classification

2. **Theme Extraction**
   - Identifies key themes from predefined categories:
     - Product Quality
     - Shipping Speed
     - Customer Service
     - Price
     - Ease of Use

3. **Response Generation**
   - Creates personalized, empathetic responses
   - Addresses specific concerns mentioned in reviews
   - Maintains professional tone

4. **Urgency Scoring**
   - Calculates review urgency based on:
     - Sentiment and confidence
     - Star rating
     - Critical themes
   - Helps prioritize customer service responses

5. **Analytics Dashboard**
   - Sentiment distribution
   - Common themes analysis
   - Top urgent reviews
   - Category-wise sentiment breakdown
   - Performance metrics

## Setup

1. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn review_ai.main:app --reload
```

## API Endpoints

### 1. Upload and Analyze Reviews

`POST /analyze/upload-json`

Upload a JSON file containing customer reviews. Each review should have:
```json
{
    "review_text": "Customer review content",
    "product_category": "Electronics",
    "star_rating": 4,
    "date_submitted": "2024-05-01"
}
```

Response format:
```json
{
    "sentiment": "Positive",
    "confidence_score": 0.95,
    "themes": ["product quality", "ease of use"],
    "response": "Thank you for your positive feedback about the product quality!",
    "urgency_score": 0.2,
    "product_category": "Electronics"
}
```

### 2. View Analytics Dashboard

`GET /dashboard`

Provides overall analytics including:
```json
{
    "sentiment_distribution": {"Positive": 25, "Neutral": 15, "Negative": 10},
    "common_themes": {"product quality": 20, "customer service": 15},
    "urgent_reviews": [...],
    "category_sentiment": {...},
    "metrics": {
        "total_reviews": 50,
        "average_confidence": 0.85,
        "average_urgency": 0.3,
        "urgent_review_ratio": 0.15
    }
}
```

## Error Handling

- Invalid JSON format: 400 Bad Request
- Missing required fields: 400 Bad Request
- Processing errors: Returns neutral sentiment with error theme
- Failed reviews: Skips individual failures, continues processing others

## Implementation Details

1. **Prompt Engineering**
   - Clear, structured prompts for consistent outputs
   - Example-based instruction for better response quality
   - Strict output format validation

2. **Data Validation**
   - Input validation using Pydantic models
   - Output sanitization for consistent responses
   - Theme validation against predefined categories

3. **Performance**
   - Uses Gemini 2.0 Flash for faster processing
   - Batch processing with error isolation
   - Efficient response parsing

## Dependencies

- FastAPI: Web framework
- Uvicorn: ASGI server
- Pydantic: Data validation
- Google Generative AI: Gemini 2.0 Flash API
- Python-dotenv: Environment management
- Python-multipart: File upload support
