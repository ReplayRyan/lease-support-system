import numpy as np

# Define functions for lease calculations probably in the phase where the training-data can be used to predict the lease metrics.
# These functions can be used to calculate lease metrics such as Present Value, Number of Periods, Monthly Payment, Lease Liability, Interest Expense, Principal Payment, Future Value, and Net Present Value.

# Calculate Present Value (PV) of Lease Payments.
def present_value(pmt, rate, nper):
    return pmt * (1 - (1 + rate) ** -nper) / rate

# Calculate Number of Periods (NPER).
def number_of_periods(pmt, rate, pv):
    return np.log(pmt / (pmt - rate * pv)) / np.log(1 + rate)

# Calculate Monthly Payment (PMT).
def monthly_payment(pv, rate, nper):
    return (pv * rate) / (1 - (1 + rate) ** -nper)

# Calculate Lease Liability as PV of lease payments.
def lease_liability(pmt, rate, nper):
    return present_value(pmt, rate, nper)

# Calculate Interest Expense per period.
def interest_expense(lease_liability, rate):
    return lease_liability * rate

# Calculate Principal Payment per period.
def principal_payment(pmt, interest_expense):
    return pmt - interest_expense

# Calculate Future Value (FV) of Lease Payments.
def future_value(pmt, rate, nper):
    return pmt * ((1 + rate) ** nper - 1) / rate

# Calculate Net Present Value (NPV) of Lease.
def net_present_value(pmt, rate, nper, initial_cost):
    return present_value(pmt, rate, nper) - initial_cost

# Perform all necessary, additional, and advanced lease calculations.
def calculate_lease_metrics(pmt, rate, nper, initial_cost):
    lease_metrics = {
        "Present Value (PV)": present_value(pmt, rate, nper),
        "Number of Periods (NPER)": number_of_periods(pmt, rate, present_value(pmt, rate, nper)),
        "Monthly Payment (PMT)": monthly_payment(present_value(pmt, rate, nper), rate, nper),
        "Lease Liability": lease_liability(pmt, rate, nper),
        "Interest Expense": interest_expense(lease_liability(pmt, rate, nper), rate),
        "Principal Payment": principal_payment(pmt, interest_expense(lease_liability(pmt, rate, nper), rate)),
        "Future Value (FV)": future_value(pmt, rate, nper),
        "Net Present Value (NPV)": net_present_value(pmt, rate, nper, initial_cost)
    }
    return lease_metrics

# Example lease details (replace with extracted values from text parsing)
pmt = 2500  # Monthly rent in USD PLACEHOLDER VALUE (You'd want to have it take the monthly rent post-parse/training-data and slot it into here.)
rate = 0.05 / 12  # Monthly interest rate (5% annual PLACEHOLDER EXAMPLE)
nper = 72  # Lease term in Months (Once again, PLACEHOLDER EXAMPLE)
initial_cost = 5000  # Security deposit in USD or other upfront cost (PLACEHOLDER EXAMPLE)

lease_results = calculate_lease_metrics(pmt, rate, nper, initial_cost)
for key, value in lease_results.items():
    print(f"{key}: {value:.2f}")