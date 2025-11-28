from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentRequest(BaseModel):
    document: str = Field(..., description="URL to the document image")


class BillItem(BaseModel):
    item_name: str = Field(..., description="Name of the item exactly as mentioned in the bill")
    item_amount: float = Field(..., description="Net amount post discounts")
    item_rate: float = Field(..., description="Rate per unit")
    item_quantity: float = Field(..., description="Quantity")
    suspicious: bool = Field(default=False, description="Flag for potential fraud")


class PagewiseLineItem(BaseModel):
    page_no: str = Field(..., description="Page number")
    page_type: str = Field(..., description="Bill Detail | Final Bill | Pharmacy")
    bill_items: List[BillItem] = Field(default_factory=list)


class TokenUsage(BaseModel):
    total_tokens: int = 0
    input_tokens: int = 0
    output_tokens: int = 0


class ExtractionData(BaseModel):
    pagewise_line_items: List[PagewiseLineItem] = Field(default_factory=list)
    total_item_count: int = 0
    reconciled_amount: float = 0.0


class APIResponse(BaseModel):
    is_success: bool
    token_usage: TokenUsage = Field(default_factory=TokenUsage)
    data: Optional[ExtractionData] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    is_success: bool = False
    message: str