# lease-support-system
The objective of this project is to develop an automated lease support system that efficiently processes lease agreements, extracts key contractual terms, and provides structured data for compliance and financial reporting. The system will assist in lease classification and support lease accounting under the ASC 842 standard.

             +------------------------------+
            |  Lease Documents (PDF, Word)  |
            +-------------------------------+
                                      │
                ┌──────────────────────────┐
                │   Document Processing    │
                ├──────────────────────────┤
                │  - AWS Textract (OCR)    │  ⬅ (If scanned PDFs)
                │  - PyMuPDF (Text Parsing)│  ⬅ (If digital PDFs)
                └──────────────────────────┘
                                      │
                ┌──────────────────────────┐
                │      NLP Processing      │
                ├──────────────────────────┤
                │  - SpaCy (NER Extraction)│
                │  - BERT (Classification) │  ⬅ (Optional for complex cases)
                └──────────────────────────┘
                                      │
                ┌──────────────────────────┐
                │    Lease Classification  │
                ├──────────────────────────┤
                │ - Python + Pandas/Numpy  │
                │ - ASC 842 Rule Engine    │
                └──────────────────────────┘
                                      │
                ┌──────────────────────────┐
                │    Data Storage & API    │
                ├──────────────────────────┤
                │           TBD            │
                └──────────────────────────┘
                                      │
                ┌───────────────────────────┐
                │      Frontend (Optional)  │
                ├───────────────────────────┤
                │ - CustomTinker            | 
                └───────────────────────────┘
