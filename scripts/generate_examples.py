import random
import datetime
import json
import re

def random_date(start_year=2024, end_year=2030):
    start = datetime.date(start_year, 1, 1)
    end = datetime.date(end_year, 12, 31)
    random_days = random.randint(0, (end - start).days)
    return (start + datetime.timedelta(days=random_days)).strftime("%B %d, %Y")

def random_rent():
    return f"${random.randint(1500, 5000):,}"

def random_security_deposit(rent):
    rent_value = int(rent.strip('$').replace(',', ''))
    multiplier = random.choice([1.5, 2, 2.5])  # Avoid 1x exactly
    deposit = int(rent_value * multiplier)
    return f"${deposit:,}"

def random_escalation_rate():
    return f"{random.choice([2, 2.5, 3, 3.5, 4])}%"

def random_termination_fee():
    return f"${random.randint(3000, 10000):,}"

def random_property_address():
    streets = ["Main St", "Market St", "Broadway", "Elm St", "Pine Ave"]
    cities = ["New York", "San Francisco", "Los Angeles", "Chicago", "Boston"]
    return f"{random.randint(100, 999)} {random.choice(streets)}, {random.choice(cities)}, NY"

templates = [
    "Lease starts on {lease_start_date} and ends on {lease_end_date}. Monthly rent: {monthly_rent}. Security deposit: {security_deposit}.",
    "Rental of {property_address} begins {lease_start_date}. Tenant pays {monthly_rent} rent and a {security_deposit} deposit.",
    "Tenant agrees to {monthly_rent} rent, escalating by {escalation_rate} annually. Security deposit required: {security_deposit}.",
    "Premises at {property_address} leased from {lease_start_date} to {lease_end_date}. Rent: {monthly_rent}.",
    "Upon signing, tenant must pay first month's rent of {monthly_rent} and a deposit of {security_deposit}.",
    "The monthly rent is {monthly_rent}, increasing yearly by {escalation_rate}. A refundable security deposit of {security_deposit} is required.",
    "A lease for {property_address} starts {lease_start_date} and ends {lease_end_date}. Termination fee: {termination_fee}.",
    "Security deposit amounting to {security_deposit} must be paid prior to occupancy.",
    "Monthly rent payments of {monthly_rent} are due on the 1st of each month.",
    "A termination fee of {termination_fee} will apply for early lease termination.",
    "Tenant agrees to {monthly_rent} rent, escalating by {escalation_rate} annually. Security deposit required: {security_deposit}.",
    "Premises at {property_address} leased from {lease_start_date} to {lease_end_date}. Rent: {monthly_rent}.",
    "Upon signing, tenant must pay first month's rent of {monthly_rent} and a deposit of {security_deposit}.",
    "The monthly rent is {monthly_rent}, increasing yearly by {escalation_rate}. A refundable security deposit of {security_deposit} is required.",
    "A lease for {property_address} starts {lease_start_date} and ends {lease_end_date}. Termination fee: {termination_fee}.",
    "This Lease Agreement is made effective as of {lease_start_date}, between the Landlord and Tenant. Tenant shall occupy the premises commencing on {lease_start_date}, with monthly rental payments of {monthly_rent} due on the first day of each month. An annual escalation rate of {escalation_rate} shall apply to the rent amount, beginning one year from the lease start date. Prior to taking possession, Tenant shall pay a security deposit of {security_deposit}, refundable upon satisfactory termination of the lease. The term of this Lease shall continue until {lease_end_date}, unless terminated earlier as provided herein. All rent payments must be made in U.S. dollars, and any failure to comply with the payment schedule will be deemed a breach of this Lease.",
    "This Residential Lease Agreement, entered into on {lease_start_date}, outlines the terms by which Tenant agrees to lease the property. Tenant shall begin occupancy on {lease_start_date} and continue through {lease_end_date}. Monthly rent is set at {monthly_rent} and is due without demand on the first of each month. Rent shall increase by {escalation_rate} annually beginning on the first anniversary of the Lease. Tenant agrees to provide a security deposit of {security_deposit} upon signing this agreement, which shall be held in escrow by the Landlord. In the event of default, the security deposit may be used to offset damages. The premises must be vacated and left in good condition upon lease termination.",
    "This agreement, effective {lease_start_date}, binds the Tenant to lease the premises under the following terms: commencement date of {lease_start_date}, expiration date of {lease_end_date}, with monthly rental payments of {monthly_rent}. A refundable security deposit of {security_deposit} is required at lease signing. The Tenant acknowledges that rent will escalate annually at a rate of {escalation_rate}. Occupancy without payment or abandonment of the premises will result in immediate legal action. Both parties agree that maintenance of the property is a joint responsibility. Renewal options may be available under terms agreed upon closer to the expiration date.",
    "On {lease_start_date}, the Tenant shall take possession of the leased premises under the following financial obligations: monthly rent in the amount of {monthly_rent}, escalating by {escalation_rate} annually, and a one-time security deposit of {security_deposit}. The term of this Lease shall end on {lease_end_date}, unless renewed. The Landlord shall ensure that the premises are delivered in good repair, and the Tenant shall maintain the property in a similar condition. Monthly rent shall be payable to the Landlord via electronic transfer or check. In the event of damage to the premises beyond normal wear and tear, the security deposit may be withheld to cover repairs. Tenant further agrees to comply with all property rules and local regulations during the lease term.",
    "Pursuant to this Lease Agreement dated {lease_start_date}, the Tenant agrees to lease the property for a term ending on {lease_end_date}. Monthly rent is established at {monthly_rent}, due and payable on the first of each month. Tenant shall provide a security deposit of {security_deposit} upon execution of this Agreement. Rent shall escalate by {escalation_rate} annually. The Landlord shall retain the security deposit in a separate account and return it within 30 days of lease termination, provided no damages or unpaid balances exist. This Agreement represents the entire understanding between the parties. Any modifications must be in writing and signed by both parties. By signing, the Tenant acknowledges having reviewed and agreed to the terms herein, including all conditions regarding rent, security deposit, and lease duration.",
    "The lease begins on {lease_start_date} and ends on {lease_end_date}. The monthly rent is {monthly_rent}, and a security deposit of {security_deposit} is required. The tenant agrees to maintain the property and abide by all regulations during the lease period. Rent will increase annually by {escalation_rate}. The tenant is also required to pay a termination fee of {termination_fee} if they choose to end the lease early.",
    "This Lease Agreement is effective as of {lease_start_date}, and the Tenant agrees to occupy the property until {lease_end_date}. Rent payments of {monthly_rent} are due each month, with an annual increase of {escalation_rate}. A security deposit of {security_deposit} is due before moving in. Tenant acknowledges that the property at {property_address} is in good condition and agrees to return it in similar condition at the end of the term. Failure to comply will result in the forfeiture of the security deposit.",
    "The tenant will start the lease on {lease_start_date}, with an end date of {lease_end_date}. The lease payment is {monthly_rent} each month, with a {escalation_rate} annual increase. The tenant is required to pay a security deposit of {security_deposit} upon signing the lease. If the tenant decides to terminate the lease before its natural expiration, a fee of {termination_fee} will be assessed. The property is located at {property_address}, and any violations of lease terms will result in immediate legal action.",
    "Occupancy will begin on {lease_start_date} for a term ending on {lease_end_date}. Rent is set at {monthly_rent} monthly, subject to an escalation rate of {escalation_rate}. The lease also includes a security deposit of {security_deposit}, which is refundable based on the condition of the property upon lease termination. The tenant has the option to renew the lease upon mutual agreement, but must notify the landlord at least 60 days prior to the end of the lease term. In case of premature termination, a termination fee of {termination_fee} will be due.",
    "As of {lease_start_date}, the tenant agrees to lease the property located at {property_address}. The rent amount is {monthly_rent}, with an annual rent increase of {escalation_rate}. A security deposit of {security_deposit} is required prior to move-in. The lease is set to terminate on {lease_end_date}, at which time the property must be returned in good condition. If the tenant wishes to terminate the lease early, a termination fee of {termination_fee} will be due. The landlord has the right to take legal action for any breaches of the lease terms.",
]

examples = []

for i in range(500):
    lease_start = random_date()
    lease_end = random_date(start_year=2031, end_year=2035)
    monthly_rent = random_rent()
    security_deposit = random_security_deposit(monthly_rent)
    escalation_rate = random_escalation_rate()
    termination_fee = random_termination_fee()
    property_address = random_property_address()

    selected_templates = random.sample(templates, 3)
    text = " ".join(template.format(
        lease_start_date=lease_start,
        lease_end_date=lease_end,
        monthly_rent=monthly_rent,
        security_deposit=security_deposit,
        escalation_rate=escalation_rate,
        termination_fee=termination_fee,
        property_address=property_address
    ) for template in selected_templates)

    used_spans = set()
    entities = []
    label_value_pairs = [
        ("LEASE_START_DATE", lease_start),
        ("LEASE_END_DATE", lease_end),
        ("MONTHLY_RENT", monthly_rent),
        ("SECURITY_DEPOSIT", security_deposit),
        ("ESCALATION_RATE", escalation_rate),
        ("TERMINATION_FEE", termination_fee),
        ("PROPERTY_ADDRESS", property_address)
    ]

    for label, value in label_value_pairs:
        pattern = re.escape(value)
        for match in re.finditer(pattern, text):
            span = (match.start(), match.end())
            if span not in used_spans:
                entities.append({
                    "start": match.start(),
                    "end": match.end(),
                    "label": label
                })
                used_spans.add(span)
                break  # Only label first occurrence to be safe

    examples.append({
        "text": text,
        "entities": entities
    })

with open("synthetic_lease_examples_fixed.json", "w") as f:
    json.dump(examples, f, indent=2)

print(f"Done: {len(examples)} examples generated safely!")
