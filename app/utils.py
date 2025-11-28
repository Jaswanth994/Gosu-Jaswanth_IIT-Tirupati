import requests
from typing import Tuple


def download_document(url: str) -> Tuple[bytes, str]:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        content_type = response.headers.get('content-type', '')
        
        if 'image/png' in content_type or url.lower().endswith('.png'):
            media_type = 'image/png'
        elif 'image/jpeg' in content_type or url.lower().endswith(('.jpg', '.jpeg')):
            media_type = 'image/jpeg'
        elif 'application/pdf' in content_type or url.lower().endswith('.pdf'):
            media_type = 'application/pdf'
        else:
            media_type = 'image/png'
        
        return response.content, media_type
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download document: {str(e)}")


def validate_extraction_result(data: dict) -> bool:
    try:
        if 'pagewise_line_items' not in data:
            return False
        
        for page in data['pagewise_line_items']:
            if 'page_no' not in page or 'bill_items' not in page:
                return False
            
            # Make page_type optional
            page.setdefault("page_type", "Unknown")

            # Validate each item
            for item in page['bill_items']:
                required_fields = ['item_name', 'item_amount', 'item_rate', 'item_quantity']
                if not all(field in item for field in required_fields):
                    return False
        
        return True
        
    except Exception:
        return False


def calculate_total_items(data: dict) -> int:
    total = 0
    for page in data.get('pagewise_line_items', []):
        total += len(page.get('bill_items', []))
    return total


def detect_duplicates(items: list) -> list:
    duplicates = []
    seen = {}
    
    for idx, item in enumerate(items):
        signature = (
            item.get('item_name', '').strip().lower(),
            float(item.get('item_rate', 0)),
            float(item.get('item_quantity', 0)),
            float(item.get('item_amount', 0))
        )
        
        if signature in seen:
            duplicates.append(idx)
        else:
            seen[signature] = idx
    
    return duplicates


def calculate_reconciled_amount(extracted_data: dict) -> float:
    total = 0.0

    for page in extracted_data.get("pagewise_line_items", []):
        for item in page.get("bill_items", []):
            try:
                total += float(item.get("item_amount", 0))
            except:
                pass

    return round(total, 2)
