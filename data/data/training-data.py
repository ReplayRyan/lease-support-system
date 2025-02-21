TRAINING_DATA = [
    ("The lease starts on January 1, 2024, and ends on December 31, 2029.",
     {"entities": [(19, 31, "LEASE_START_DATE"), (42, 56, "LEASE_END_DATE")]}),

    ("The monthly rent is $2,500, with a fixed escalation of 5%.",
     {"entities": [(21, 26, "RENT_AMOUNT"), (55, 58, "ESCALATION_RATE")]}),

    ("The lease is for an office space located at 123 Main St, New York, NY.",
     {"entities": [(29, 59, "PROPERTY_ADDRESS")]}),

    ("The tenant has an option to renew for an additional 5 years.",
     {"entities": [(18, 32, "RENEWAL_CLAUSE")]}),

    ("A security deposit of $5,000 is required before moving in.",
     {"entities": [(22, 27, "SECURITY_DEPOSIT")]}),

    ("The lease will automatically terminate on December 31, 2030.",
     {"entities": [(40, 54, "LEASE_END_DATE")]}),

    ("Base rent is set at $3,200 per month, subject to annual CPI increases.",
     {"entities": [(18, 23, "RENT_AMOUNT")]}),

    ("An early termination fee of $10,000 applies if the lease is broken before two years.",
     {"entities": [(29, 36, "TERMINATION_FEE")]}),
]