import re
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from datetime import datetime, date
from typing import Optional, Tuple


class OCRService:
    """Service for extracting text and data from receipt images using Tesseract OCR."""
    
    def __init__(self):
        # Common date formats found on receipts
        self.date_patterns = [
            r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
            r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
            r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
            r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        ]
        
        # Common total indicators
        self.total_keywords = [
            'total', 'amount', 'sum', 'balance', 'due',
            'grand total', 'subtotal', 'amount due'
        ]
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image to improve OCR accuracy.
        
        Steps:
        1. Convert to grayscale
        2. Enhance contrast
        3. Apply slight sharpening
        4. Denoise
        """
        # Convert to grayscale
        image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Sharpen
        image = image.filter(ImageFilter.SHARPEN)
        
        # Denoise
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    
    def extract_text(self, image_path: str) -> str:
        """Extract raw text from image using Tesseract OCR."""
        try:
            image = Image.open(image_path)
            processed_image = self.preprocess_image(image)
            
            # Use Tesseract with custom config for better receipt recognition
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            return text
        except Exception as e:
            raise Exception(f"OCR extraction failed: {str(e)}")
    
    def extract_merchant(self, text: str) -> Optional[str]:
        """
        Extract merchant name from receipt text.
        Typically the first capitalized line or largest text.
        """
        lines = text.strip().split('\n')
        
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Look for lines with mostly uppercase and at least 3 chars
            if len(line) >= 3 and sum(1 for c in line if c.isupper()) > len(line) * 0.5:
                # Clean up the merchant name
                merchant = re.sub(r'[^a-zA-Z0-9\s&\'-]', '', line)
                if merchant:
                    return merchant[:100]  # Limit to 100 chars
        
        return "Unknown Merchant"
    
    def extract_amount(self, text: str) -> Optional[float]:
        """
        Extract total amount from receipt text.
        Looks for amounts near 'total' keywords or largest amount.
        """
        # Find all amounts in format: $XX.XX or XX.XX
        amount_pattern = r'\$?\s*(\d+[,.]?\d*\.?\d{2})'
        amounts = []
        
        lines = text.lower().split('\n')
        
        for line in lines:
            # Check if line contains total keyword
            is_total_line = any(keyword in line for keyword in self.total_keywords)
            
            # Find all amounts in this line
            matches = re.findall(amount_pattern, line)
            
            for match in matches:
                # Clean the amount string
                amount_str = match.replace(',', '').replace(' ', '')
                try:
                    amount = float(amount_str)
                    # Prioritize amounts from total lines
                    weight = 10 if is_total_line else 1
                    amounts.append((amount, weight))
                except ValueError:
                    continue
        
        if not amounts:
            return None
        
        # Sort by weight (total lines first) then by amount (largest first)
        amounts.sort(key=lambda x: (x[1], x[0]), reverse=True)
        
        return amounts[0][0] if amounts else None
    
    def extract_date(self, text: str) -> Optional[date]:
        """
        Extract date from receipt text.
        Tries multiple common date formats.
        """
        for pattern in self.date_patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(0)
                
                # Try to parse the date
                for fmt in ['%m/%d/%Y', '%m-%d-%Y', '%Y/%m/%d', '%Y-%m-%d']:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt).date()
                        # Sanity check: date shouldn't be in the future or too old
                        if parsed_date <= date.today() and parsed_date.year >= 2000:
                            return parsed_date
                    except ValueError:
                        continue
        
        # Default to today if no date found
        return date.today()
    
    def guess_category(self, merchant: str, text: str) -> str:
        """
        Simple category guessing based on merchant name and text content.
        """
        text_lower = text.lower()
        merchant_lower = merchant.lower()
        
        # Food & Dining
        food_keywords = ['restaurant', 'cafe', 'coffee', 'pizza', 'burger', 'food', 'dine']
        if any(kw in merchant_lower or kw in text_lower for kw in food_keywords):
            return 'food'
        
        # Groceries
        grocery_keywords = ['market', 'grocery', 'supermarket', 'whole foods', 'trader']
        if any(kw in merchant_lower for kw in grocery_keywords):
            return 'groceries'
        
        # Transportation
        transport_keywords = ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'parking']
        if any(kw in merchant_lower for kw in transport_keywords):
            return 'transport'
        
        # Entertainment
        entertainment_keywords = ['cinema', 'theater', 'movie', 'game', 'spotify', 'netflix']
        if any(kw in merchant_lower for kw in entertainment_keywords):
            return 'entertainment'
        
        # Shopping
        shopping_keywords = ['amazon', 'store', 'shop', 'mart', 'target', 'walmart']
        if any(kw in merchant_lower for kw in shopping_keywords):
            return 'shopping'
        
        # Default
        return 'other'
    
    def process_receipt(self, image_path: str) -> Tuple[dict, float, str]:
        """
        Process receipt image and extract expense data.
        
        Returns:
            Tuple of (expense_data, confidence, raw_text)
        """
        # Extract raw text
        raw_text = self.extract_text(image_path)
        
        if not raw_text.strip():
            raise Exception("No text could be extracted from image")
        
        # Extract individual fields
        merchant = self.extract_merchant(raw_text)
        amount = self.extract_amount(raw_text)
        receipt_date = self.extract_date(raw_text)
        category = self.guess_category(merchant, raw_text)
        
        if amount is None:
            raise Exception("Could not extract amount from receipt")
        
        # Calculate confidence score (simple heuristic)
        confidence = 0.5  # Base confidence
        
        if merchant and merchant != "Unknown Merchant":
            confidence += 0.2
        if amount:
            confidence += 0.2
        if receipt_date != date.today():  # Found actual date
            confidence += 0.1
        
        confidence = min(confidence, 1.0)
        
        expense_data = {
            "merchant": merchant,
            "amount": round(amount, 2),
            "category": category,
            "date": receipt_date,
            "notes": "Imported from receipt via OCR"
        }
        
        return expense_data, confidence, raw_text


# Singleton instance
ocr_service = OCRService()