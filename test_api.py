import requests
import json


def test_api(base_url="http://localhost:8000"):
    """Test the bill extraction API"""
    
    # Test documents
    test_documents = [
        {
            "name": "Sample 1 - Pharmacy Bill",
            "url": "https://hackrx.blob.core.windows.net/assets/datathon-IIT/sample_2.png?sv=2025-07-05&spr=https&st=2025-11-24T14%3A13%3A22Z&se=2026-11-25T14%3A13%3A00Z&sr=b&sp=r&sig=WFJYfNw0PJdZOpOYlsoAW0XujYGG1x2HSbcDREiFXSU%3D"
        },
        {
            "name": "Sample 2 - Hospital Bill",
            "url": "https://hackrx.blob.core.windows.net/assets/datathon-IIT/sample_3.png?sv=2025-07-05&spr=https&st=2025-11-24T14%3A24%3A39Z&se=2026-11-25T14%3A24%3A00Z&sr=b&sp=r&sig=egKAmIUms8H5f3kgrGXKvcfuBVlQp0Qc2tsfxdvRgUY%3D"
        }
    ]
    
    print("=" * 60)
    print("Testing Medical Bill Extraction API")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Health check error: {str(e)}")
    
    # Test extraction endpoint
    for idx, doc in enumerate(test_documents, 1):
        print(f"\n{idx + 1}. Testing extraction: {doc['name']}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{base_url}/extract-bill-data",
                json={"document": doc["url"]},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get("is_success"):
                    print("✓ Extraction successful")
                    print(f"  Total items extracted: {result['data']['total_item_count']}")
                    print(f"  Token usage: {result['token_usage']['total_tokens']}")
                    
                    # Display extracted items
                    for page in result['data']['pagewise_line_items']:
                        print(f"\n  Page {page['page_no']} ({page['page_type']}):")
                        for item in page['bill_items'][:5]:  # Show first 5 items
                            print(f"    - {item['item_name']}: "
                                  f"₹{item['item_amount']} "
                                  f"(Rate: ₹{item['item_rate']}, Qty: {item['item_quantity']})")
                        
                        if len(page['bill_items']) > 5:
                            print(f"    ... and {len(page['bill_items']) - 5} more items")
                    
                    # Calculate total
                    total_amount = sum(
                        item['item_amount'] 
                        for page in result['data']['pagewise_line_items']
                        for item in page['bill_items']
                    )
                    print(f"\n  Total Bill Amount: ₹{total_amount:.2f}")
                    
                else:
                    print(f"✗ Extraction failed: {result.get('message')}")
            else:
                print(f"✗ Request failed: {response.status_code}")
                print(f"  Response: {response.text}")
                
        except Exception as e:
            print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Testing completed")
    print("=" * 60)


def validate_response_format(response_data):
    """Validate if response matches expected format"""
    required_fields = ['is_success', 'token_usage', 'data']
    
    for field in required_fields:
        if field not in response_data:
            return False, f"Missing field: {field}"
    
    if response_data['is_success']:
        data = response_data['data']
        if 'pagewise_line_items' not in data or 'total_item_count' not in data:
            return False, "Invalid data structure"
    
    return True, "Valid format"


if __name__ == "__main__":
    import sys
    
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    test_api(base_url)