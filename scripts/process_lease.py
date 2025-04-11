# scripts/process_lease.py

from scripts.pdf_parser import extract_text_from_pdf_file
from scripts.calculations import calculate_lease_metrics
from scripts.test_ner import extract_entities  # Import the NER extraction function
from datetime import datetime
from dateutil import parser  # Add this import for flexible date parsing

def clean_lease_data(lease_data):
    """
    Cleans and validates lease data extracted from text.
    Prompts the user for missing or misclassified data if necessary.
    """
    print(f"Raw Lease Data Before Cleaning: {lease_data}")  # Debugging output

    # Prompt for missing or misclassified monthly rent
    if lease_data.get("monthly_rent") is None or not isinstance(lease_data["monthly_rent"], (int, float)):
        try:
            lease_data["monthly_rent"] = float(input("Monthly rent could not be extracted or is invalid. Please enter the monthly rent (e.g., 2500): "))
        except ValueError:
            raise ValueError("Invalid input for monthly rent. Please enter a numeric value.")

    # Prompt for missing or misclassified lease start date
    if lease_data.get("lease_start_date") is None:
        lease_data["lease_start_date"] = input("Lease start date could not be extracted. Please enter the lease start date (e.g., MM/DD/YYYY or January 15, 2025): ")

    # Prompt for missing or misclassified lease end date
    if lease_data.get("lease_end_date") is None:
        lease_data["lease_end_date"] = input("Lease end date could not be extracted. Please enter the lease end date (e.g., MM/DD/YYYY or January 15, 2025): ")

    # Parse and normalize dates to a consistent format
    while True:
        try:
            lease_data["lease_start_date"] = parser.parse(lease_data["lease_start_date"]).strftime("%m/%d/%Y")
            break
        except Exception:
            lease_data["lease_start_date"] = input("Invalid lease start date format. Please re-enter the lease start date (e.g., MM/DD/YYYY or January 15, 2025): ")

    while True:
        try:
            lease_data["lease_end_date"] = parser.parse(lease_data["lease_end_date"]).strftime("%m/%d/%Y")
            break
        except Exception:
            lease_data["lease_end_date"] = input("Invalid lease end date format. Please re-enter the lease end date (e.g., MM/DD/YYYY or January 15, 2025): ")

    # Calculate lease term in months if not already calculated
    if "lease_term_months" not in lease_data or lease_data["lease_term_months"] is None:
        try:
            start = datetime.strptime(lease_data["lease_start_date"], "%m/%d/%Y")
            end = datetime.strptime(lease_data["lease_end_date"], "%m/%d/%Y")
            lease_data["lease_term_months"] = (end.year - start.year) * 12 + (end.month - start.month)
        except Exception as e:
            raise ValueError(f"Error calculating lease term: {e}")

    print(f"Cleaned Lease Data: {lease_data}")  # Debugging output
    return lease_data

def process_lease(pdf_file_path, interest_rate=0.05, initial_cost=5000):
    try:
        # Step 1: Extract raw text from PDF
        text = extract_text_from_pdf_file(pdf_file_path)
        print(f"Extracted Text:\n{text}")  # Debugging output

        # Step 2: Use SpaCy NER model to extract structured data
        lease_data = extract_entities(text)
        print(f"Parsed Lease Data (via SpaCy): {lease_data}")  # Debugging output

        # Step 3: Clean and validate
        lease_data = clean_lease_data(lease_data)
        print(f"Cleaned Lease Data: {lease_data}")  # Debugging output

        # Step 4: Perform financial calculations
        rate = float(interest_rate) / 12  # Convert annual rate to monthly
        pmt = float(lease_data["monthly_rent"])
        nper = int(lease_data["lease_term_months"])

        # Validate inputs before calculations
        if not isinstance(pmt, (int, float)) or pmt <= 0:
            raise ValueError(f"Invalid monthly rent (PMT): {pmt}")
        if not isinstance(rate, (int, float)) or rate <= 0:
            raise ValueError(f"Invalid interest rate: {rate}")
        if not isinstance(nper, int) or nper <= 0:
            raise ValueError(f"Invalid number of periods (NPER): {nper}")

        print(f"Inputs to calculate_lease_metrics - PMT: {pmt}, Rate: {rate}, NPER: {nper}, Initial Cost: {initial_cost}")  # Debugging output

        lease_metrics = calculate_lease_metrics(
            pmt=pmt,
            rate=rate,
            nper=nper,
            initial_cost=initial_cost
        )
        print(f"Lease Metrics: {lease_metrics}")  # Debugging output

        return {
            "lease_data": lease_data,
            "lease_metrics": lease_metrics
        }
    except Exception as e:
        raise RuntimeError(f"Error processing lease: {e}")
