import fitz  # PyMuPDF

def extract_text_from_pdf_file(file_path):
    """
    Extracts text from a PDF file given its file path.
    
    Args:
        file_path (str): The path to the PDF file.
    
    Returns:
        str: The extracted text from the PDF.
    """
    text = ""
    with fitz.open(file_path) as doc:  # Open PDF from file path
        for page in doc:
            text += page.get_text("text") + "\n"  # Extract text from each page
    return text

def extract_text_from_pdf(text):
    """
    Parses raw text extracted from a PDF into structured lease data.
    
    Args:
        text (str): The raw text extracted from the PDF.
    
    Returns:
        dict: A dictionary containing structured lease data.
    """
    lease_data = {}
    try:
        for line in text.splitlines():
            line = line.strip()
            if "Lease Start Date" in line:
                lease_data["lease_start_date"] = line.split(":", 1)[1].strip()
            elif "Lease End Date" in line:
                lease_data["lease_end_date"] = line.split(":", 1)[1].strip()
            elif "Monthly Rent" in line:
                # Handle variations in formatting for monthly rent
                rent_value = line.split(":", 1)[1].strip()
                lease_data["monthly_rent"] = float(
                    rent_value.replace("$", "").replace(",", "").strip()
                )
    except Exception as e:
        raise ValueError(f"Error parsing lease data: {e}")
    
    # print(f"Extracted Lease Data: {lease_data}")  # Debugging output
    return lease_data
