import anthropic
import base64
import json
import os
from typing import Dict, Any
from .models import ExtractionData, TokenUsage


class BillExtractor:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
        
    def extract_from_image(self, image_data: bytes, media_type: str) -> Dict[str, Any]:
        """
        Extract bill data from image using Claude Vision API
        """
        # Convert image to base64
        base64_image = base64.standard_b64encode(image_data).decode("utf-8")
        
        # Prepare the extraction prompt
        extraction_prompt = self._get_extraction_prompt()
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": extraction_prompt
                            }
                        ],
                    }
                ],
            )
            
            # Extract token usage
            token_usage = TokenUsage(
                total_tokens=message.usage.input_tokens + message.usage.output_tokens,
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens
            )
            
            # Parse response
            response_text = message.content[0].text
            
            # Extract JSON from response (handle markdown code blocks)
            json_str = self._extract_json(response_text)
            result = json.loads(json_str)
            
            return {
                "success": True,
                "data": result,
                "token_usage": token_usage
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "token_usage": TokenUsage()
            }
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text, handling markdown code blocks"""
        text = text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        
        if text.endswith("```"):
            text = text[:-3]
        
        return text.strip()
    
    def _get_extraction_prompt(self) -> str:
        """Get the extraction prompt for Claude"""
        return """You are an expert medical bill extraction system. Analyze this bill image and extract ALL line items with perfect accuracy.

**EXTRACTION RULES:**
1. Extract EVERY line item visible in the bill
2. Use EXACT item names as printed (no normalization)
3. Extract item_rate (per unit rate), item_quantity, and item_amount (total after discounts)
4. DO NOT extract subtotals or section totals as items
5. Detect and mark suspicious entries (font inconsistencies, overwriting, etc.)
6. Page type must be: "Bill Detail", "Final Bill", or "Pharmacy"
7. Ensure NO duplicate items and NO missing items

**CRITICAL:** 
- If quantity is not shown, assume 1.0
- If rate equals amount, quantity is 1.0
- item_amount = item_rate × item_quantity (after discounts)
- Preserve all decimals and exact numbers

**OUTPUT FORMAT (JSON only, no explanation):**
```json
{
  "pagewise_line_items": [
    {
      "page_no": "1",
      "page_type": "Bill Detail",
      "bill_items": [
        {
          "item_name": "Consultation Charge",
          "item_amount": 500.00,
          "item_rate": 500.00,
          "item_quantity": 1.0,
          "suspicious": false
        }
      ]
    }
  ],
  "total_item_count": 1
}
```

Analyze the image now and return ONLY the JSON:"""