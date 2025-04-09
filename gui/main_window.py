import sys
import os
import importlib.util
from customtkinter import *
from tkinter import filedialog
import subprocess

# Dynamically load calculations.py from processing directory
processing_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../processing/calculations.py"))
spec = importlib.util.spec_from_file_location("calculations", processing_path)
calculations = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calculations)


# App setup
set_appearance_mode("system")
set_default_color_theme("blue")

app = CTk()
app.geometry("1000x800")
app.title("Lease NER Extractor")
app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

# ========== Global variable ==========
original_ner_output = {}

# ========== Functions ==========

def upload_pdf():
    global original_ner_output

    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        file_name = os.path.basename(file_path)
        file_label.configure(text=f"📄 {file_name}")
        print(f"PDF selected: {file_path}")

        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts/test_ner.py"))
        print(f"Running script from: {script_path}")

        try:
            result = subprocess.run([sys.executable, script_path, file_path], capture_output=True, text=True, check=True)

            extracted_values = parse_ner_output(result.stdout)
            original_ner_output = extracted_values
            update_given_info(extracted_values)

            print("Script executed and fields updated.")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error running script:\n{e.stderr}")

def parse_ner_output(ner_output):
    return {
        "Rent Amount": 100000,
        "Lease Term": 60,
        "Interest Rate": 0.05
    }

def update_given_info(extracted_values):
    rent_entry.delete(0, "end")
    rent_entry.insert(0, extracted_values["Rent Amount"])

    lease_term_entry.delete(0, "end")
    lease_term_entry.insert(0, extracted_values["Lease Term"])

    interest_rate_entry.delete(0, "end")
    interest_rate_entry.insert(0, extracted_values["Interest Rate"])

def restore_pdf_values():
    if original_ner_output:
        update_given_info(original_ner_output)
        print("Restored original PDF values.")
    else:
        print("No original NER values to restore.")

def calculate_information():
    pmt = float(rent_entry.get())
    rate = float(interest_rate_entry.get()) / 12
    nper = int(lease_term_entry.get())
    initial_cost = 5000  # Placeholder

    lease_metrics = calculations.calculate_lease_metrics(pmt, rate, nper, initial_cost)

    present_value_entry.delete(0, "end")
    present_value_entry.insert(0, f"{lease_metrics['Present Value (PV)']:.2f}")

    monthly_payment_entry.delete(0, "end")
    monthly_payment_entry.insert(0, f"{lease_metrics['Monthly Payment (PMT)']:.2f}")

    lease_liability_entry.delete(0, "end")
    lease_liability_entry.insert(0, f"{lease_metrics['Lease Liability']:.2f}")

    interest_expense_entry.delete(0, "end")
    interest_expense_entry.insert(0, f"{lease_metrics['Interest Expense']:.2f}")

    principal_payment_entry.delete(0, "end")
    principal_payment_entry.insert(0, f"{lease_metrics['Principal Payment']:.2f}")

    future_value_entry.delete(0, "end")
    future_value_entry.insert(0, f"{lease_metrics['Future Value (FV)']:.2f}")

    net_present_value_entry.delete(0, "end")
    net_present_value_entry.insert(0, f"{lease_metrics['Net Present Value (NPV)']:.2f}")

def open_settings():
    settings_app = CTk()
    settings_app.geometry("420x400")
    settings_app.title("⚙ Application Settings")

    current_font_size = IntVar(value=12)

    def change_appearance(choice):
        set_appearance_mode(choice.lower())
        print(f"Appearance mode set to {choice}")

    def change_theme(choice):
        set_default_color_theme(choice.lower())
        print(f"Color theme set to {choice}")

    def reset_to_default():
        appearance_option.set("Dark")
        theme_option.set("Blue")
        set_appearance_mode("dark")
        set_default_color_theme("blue")
        print("✅ Settings reset to default.")

    main_frame = CTkFrame(settings_app)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    title = CTkLabel(main_frame, text="Settings", font=("Helvetica", 18, "bold"))
    title.pack(pady=(10, 20))

    appearance_option = StringVar(value="System")
    appearance_label = CTkLabel(main_frame, text="Appearance Mode")
    appearance_label.pack(anchor="w")
    appearance_dropdown = CTkOptionMenu(main_frame, variable=appearance_option, values=["System", "Dark", "Light"], command=change_appearance)
    appearance_dropdown.pack(fill="x", pady=5)

    theme_option = StringVar(value="Blue")
    theme_label = CTkLabel(main_frame, text="Color Theme")
    theme_label.pack(anchor="w", pady=(10, 0))
    theme_dropdown = CTkOptionMenu(main_frame, variable=theme_option, values=["Blue", "Green", "Dark-Blue"], command=change_theme)
    theme_dropdown.pack(fill="x", pady=5)

    reset_btn = CTkButton(main_frame, text="Reset to Default", command=reset_to_default, fg_color="#D9534F", hover_color="#C9302C")
    reset_btn.pack(pady=20)

    settings_app.mainloop()

# ========== UI Layout ==========

main_frame = CTkScrollableFrame(app, label_text="", width=800)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

header = CTkLabel(main_frame, text="Lease Entity Extractor", font=("Helvetica", 20, "bold"))
header.pack(pady=20)

upload_frame = CTkFrame(main_frame)
upload_frame.pack(pady=10, fill="x")

upload_btn = CTkButton(upload_frame, text="📤 Upload PDF", command=upload_pdf)
upload_btn.pack(side="left", padx=10)

file_label = CTkLabel(upload_frame, text="No file selected", text_color="gray")
file_label.pack(side="left", padx=10)

# ========== GIVEN INFO ==========

given_info_frame = CTkFrame(main_frame)
given_info_frame.pack(pady=10, padx=20, fill="x")

given_info_label = CTkLabel(given_info_frame, text="GIVEN INFORMATION (Editable)", font=("Helvetica", 16, "bold"))
given_info_label.grid(row=0, column=0, columnspan=2, pady=10)

rent_label = CTkLabel(given_info_frame, text="Rent Amount:")
rent_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
rent_entry = CTkEntry(given_info_frame)
rent_entry.grid(row=1, column=1, padx=5, pady=5)

lease_term_label = CTkLabel(given_info_frame, text="Lease Term (Months):")
lease_term_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
lease_term_entry = CTkEntry(given_info_frame)
lease_term_entry.grid(row=2, column=1, padx=5, pady=5)

interest_rate_label = CTkLabel(given_info_frame, text="Interest Rate (Annual %):")
interest_rate_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)
interest_rate_entry = CTkEntry(given_info_frame)
interest_rate_entry.grid(row=3, column=1, padx=5, pady=5)

restore_btn = CTkButton(given_info_frame, text="Restore Default PDF Values", command=restore_pdf_values)
restore_btn.grid(row=4, column=0, columnspan=2, pady=10)

# ========== CALCULATED INFO ==========

calculated_info_frame = CTkFrame(main_frame)
calculated_info_frame.pack(pady=10, padx=20, fill="x")

calculated_info_label = CTkLabel(calculated_info_frame, text="CALCULATED INFORMATION (Editable)", font=("Helvetica", 16, "bold"))
calculated_info_label.grid(row=0, column=0, columnspan=2, pady=10)

labels = [
    ("Present Value (PV):", lambda: present_value_entry),
    ("Monthly Payment (PMT):", lambda: monthly_payment_entry),
    ("Lease Liability:", lambda: lease_liability_entry),
    ("Interest Expense:", lambda: interest_expense_entry),
    ("Principal Payment:", lambda: principal_payment_entry),
    ("Future Value (FV):", lambda: future_value_entry),
    ("Net Present Value (NPV):", lambda: net_present_value_entry)
]

for i, (text, entry_fn) in enumerate(labels, start=1):
    lbl = CTkLabel(calculated_info_frame, text=text)
    lbl.grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry = CTkEntry(calculated_info_frame)
    entry.grid(row=i, column=1, padx=5, pady=5)
    globals()[entry_fn.__name__.split('_')[0] + '_entry'] = entry

calculate_btn = CTkButton(calculated_info_frame, text="Calculate Lease Information", command=calculate_information)
calculate_btn.grid(row=8, column=0, columnspan=2, pady=10)

# ========== SETTINGS BUTTON ==========
settings_btn = CTkButton(app, text="⚙️ Settings", command=open_settings)
settings_btn.pack(pady=10)

# ========== RUN ==========
app.mainloop()
