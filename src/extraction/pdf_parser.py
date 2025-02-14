import pymupdf
import tkinter as tk
from tkinter import filedialog

def extract_text_from_pdf(filename):
    text = ""
    doc = pymupdf.open(filename)  # or pymupdf.Document(filename)

    for page in doc:
        text += page.get_text("text") + "\n"  # Extract text from each page

    return text


root = tk.Tk()
root.withdraw()  # Hide the main window
filename = filedialog.askopenfilename(title="Select Lease Agreement", filetypes=[("PDF Files", "*.pdf")])

if filename:  # If a file was selected
    print(f"Selected File: {filename}")
else:
    print("No file selected!")


extracted_text = extract_text_from_pdf(filename)
print(extracted_text)  # Prints extracted text