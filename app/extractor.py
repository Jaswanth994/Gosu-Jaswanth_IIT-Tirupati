import google.generativeai as genai
import base64
import json
import os
from typing import Dict, Any
from .models import TokenUsage


class BillExtractor:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)

        # Correct model for vision extraction
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def extract_from_image(self, image_data: bytes, media_type: str) -> Dict[str, Any]:
        """
        Extract bill data using Gemini Vision.
        """
        prompt = self._get_extraction_prompt()

        try:
            response = self.model.generate_content(
                [
                    prompt,
                    {
                        "mime_type": media_type,
                        "data": image_data
                    }
                ],
                generation_config={"max_output_tokens": 4000}
            )

            response_text = response.text

            # Fix markdown issues
            json_str = self._extract_json(response_text)
            result = json.loads(json_str)

            token_usage = TokenUsage(
                total_tokens=0,
                input_tokens=0,
                output_tokens=0
            )

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
        """Extract JSON from text."""
        text = text.strip()

        if text.startswith("```json"):
            text = text[len("```json"):]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()

    def _get_extraction_prompt(self) -> str:
        return """
You are an expert medical bill extraction engine. Extract all line items.

Return ONLY this JSON:

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
          "item_quantity": 1.0
        }
      ]
    }
  ],
  "total_item_count": 1
}

Rules:
- EXACT item names.
- Extract rate, quantity, amount.
- No subtotals.
- No totals.
- No duplications.
- No missing items.
- If quantity missing → 1.0
- Page_type must be: Bill Detail, Final Bill, or Pharmacy.
Return ONLY JSON.
"""
