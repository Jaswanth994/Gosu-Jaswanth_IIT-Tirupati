from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .models import (
    DocumentRequest, 
    APIResponse, 
    ErrorResponse,
    ExtractionData,
    TokenUsage
)
from .extractor import BillExtractor
from .utils import (
    download_document,
    validate_extraction_result,
    calculate_total_items
)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Medical Bill Extraction API",
    description="Extract line items from medical bills with high accuracy",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize extractor
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

extractor = BillExtractor(api_key=ANTHROPIC_API_KEY)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Medical Bill Extraction API is running",
        "version": "1.0.0"
    }


@app.post("/extract-bill-data", response_model=APIResponse)
async def extract_bill_data(request: DocumentRequest):
    """
    Extract bill line items from a document URL
    
    Args:
        request: DocumentRequest containing the document URL
        
    Returns:
        APIResponse with extracted bill data or error message
    """
    try:
        # Step 1: Download the document
        try:
            image_data, media_type = download_document(request.document)
        except Exception as e:
            return APIResponse(
                is_success=False,
                message=f"Failed to download document: {str(e)}"
            )
        
        # Step 2: Extract data using Claude
        result = extractor.extract_from_image(image_data, media_type)
        
        if not result["success"]:
            return APIResponse(
                is_success=False,
                message=f"Extraction failed: {result.get('error', 'Unknown error')}",
                token_usage=result["token_usage"]
            )
        
        # Step 3: Validate and structure the response
        extracted_data = result["data"]
        
        if not validate_extraction_result(extracted_data):
            return APIResponse(
                is_success=False,
                message="Extraction result validation failed",
                token_usage=result["token_usage"]
            )
        
        # Calculate total item count
        total_items = calculate_total_items(extracted_data)
        extracted_data["total_item_count"] = total_items
        
        # Step 4: Return successful response
        return APIResponse(
            is_success=True,
            token_usage=result["token_usage"],
            data=ExtractionData(**extracted_data)
        )
        
    except Exception as e:
        # Handle unexpected errors
        return APIResponse(
            is_success=False,
            message=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api_key_configured": bool(ANTHROPIC_API_KEY),
        "model": "claude-sonnet-4-20250514"
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)