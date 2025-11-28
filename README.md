
---

# 🧾 README.md


# 🏥 Medical Bill Extraction API (OPD/IPD)

AI-powered API for extracting detailed line items from multi-page medical invoices.  
Built for **Bajaj Finserv Health Datathon 2025** using **Google Gemini-2.5-Flash Vision**.

---

## 🚀 Overview

This API extracts:

- Line item details  
- Page-wise classification  
- Rate, quantity, amount  
- Total item count  
- Suspicious/fraud indicators  
- Works for PDFs, PNG, JPG  

The system is designed for real-world insurance claim processing workflows.

---

## 🧠 Problem Statement

Healthcare insurers process thousands of bills daily. These bills:

- Are long (5–40 pages)  
- Contain mixed sections (pharmacy, lab, consultation)  
- Have complex tables  
- Include handwriting or altered text  
- Require 100% accurate extraction  

This API automatically extracts **all line items**, ensuring:

- No missing items  
- No double-counting  
- Correct totals  
- Fraud/suspicious detection  

---

## ⚙️ Features

### ✔ High-accuracy extraction
Extracts item name, rate, quantity, amount with precision.

### ✔ Page-wise categorization
- Bill Detail  
- Pharmacy  
- Final Bill  

### ✔ Fraud Detection  
Flags:
- Overwritten values  
- Font inconsistencies  
- Tampered digits  

### ✔ Supports multiple formats  
- PNG  
- JPG  
- PDF (single/multi-page)  

### ✔ Model Used  
**Google Gemini-2.5-Flash Vision**  
- Multimodal  
- Fast  
- Free tier  
- Highly accurate for documents  

---

## 🧩 Architecture

```

┌──────────────┐      ┌──────────────┐      ┌──────────────────────────┐
│   Client      │ ───▶ │   FastAPI     │ ───▶ │ Gemini-2.5-Flash Vision │
└──────────────┘      └──────────────┘      └──────────────────────────┘
│
▼
┌──────────────────┐
│ Post-Processing  │
└──────────────────┘

```

---

## 📁 Project Structure

```

project_root/
│── app/
│   │── main.py
│   │── extractor.py
│   │── models.py
│   │── utils.py
│── run.py
│── requirements.txt
│── README.md

````

---

## 🔧 Installation

### 1. Clone the repository
```bash
git clone <repo-url>
cd <project>
````

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a file named `.env`:

```
GEMINI_API_KEY=YOUR_GOOGLE_GEMINI_KEY
PORT=8000
```

Get free key at:
➡ [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)

---

## ▶️ Running Locally

Start FastAPI server:

```bash
python run.py
```

Server runs at:

```
http://localhost:8000
```

Docs:

```
http://localhost:8000/docs
```

---

## 🔥 API Endpoint

### **POST /extract-bill-data**

### Request

```json
{
  "document": "https://example.com/bill.png"
}
```

### Response

```json
{
  "is_success": true,
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "page_type": "Pharmacy",
        "bill_items": [
          {
            "item_name": "Pantocid DSR",
            "item_amount": 145.00,
            "item_rate": 72.50,
            "item_quantity": 2.0,
            "suspicious": false
          }
        ]
      }
    ],
    "total_item_count": 12
  },
  "token_usage": {
    "total_tokens": 0,
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

---

## 🧪 Testing

### Postman

Send POST request with document URL.

### Curl

```bash
curl -X POST https://your-app.onrender.com/extract-bill-data \
-H "Content-Type: application/json" \
-d '{"document": "<image_url>"}'
```

---

## ☁️ Deployment (Render)

### Build command

```
pip install -r requirements.txt
```

### Start command

```
python run.py
```

### Environment variables

```
GEMINI_API_KEY=your_key_here
```

Your live API will be:

```
https://yourapp.onrender.com/extract-bill-data
```

---

## 📈 Performance

| Metric            | Result             |
| ----------------- | ------------------ |
| Latency           | 2–4s               |
| Accuracy          | 90–95%             |
| Cost              | FREE (Gemini tier) |
| Supported Formats | PNG, JPG, PDF      |

---

## 💡 Challenges Solved

* Unstructured, multi-format bills
* Multi-page extraction
* No double counting
* Suspicious entry detection
* Handwriting/low-quality readability

---

## 👨‍💻 Author

**Gosu Jaswanth**
IIT Tirupati
Bajaj Finserv Health Datathon 2025

---


