Completed Track: Practo (Healthcare)

Domain Selection: This project implements the Practo (Healthcare Support) domain.

The assistant supports:

Appointment booking policies
Appointment cancellation policies
Appointment rescheduling policies
Consultation fees
Insurance claim policies
Prescription refill workflows
Laboratory result timelines
Telemedicine eligibility
Emergency visit procedures
Privacy and patient data protection
Appointment record lookup

Dataset Generation
Dataset size: 50 random appointments
Random Seed: 42

CATEGORIES and WEIGHTS
    "General Medicine" : 0.30
    "Cardiology" : 0.20
    "Dermatology" : 0.15
    "Pediatrics" : 0.15
    "Orthopedics" : 0.20

STATUSES AND STATUS WEIGHTS
    "Scheduled" : 0.25
    "Completed" : 0.40
    "Cancelled" : 0.10
    "No-Show" : 0.05
    "Rescheduled" : 0.20

FOLLOW_UP_PROBABILITY: 0.20

MIN_FEE: 300
MAX_FEE: 2500
Fee Rationale: Realistic approximation of outpatient consultation fee across multiple specialities in urban areas


KNOWLEDGE BASE POLICIES
    Appointment Booking policy: appointment_booking.md
    Appointment Cancellation policy: appointment_cancellation.md
    Appointment Rescheduling Policy: appointment_rescheduling.md
    Consultation Fee policy: consultation_fees.md
    Insurance Claims policy: insurance_claims.md
    Telemedicine policy: telemedicine_policy.md
    Lab Turnaround policy: lab_turnaround.md
    Prescription Refill policy: prescription_refills.md
    Follow-up Discount policy: follow_up_discounts.md
    Home Visit Eligibility policy: home_visit_eligibility.md
    Emergency Visit Protocol: emergency_visit_protocol.md
    Data Privacy policy: data_privacy.md
    Payment Refund policy: payment_refunds.md
    Second Opinion Process: second_opinion_process.md
    Patient Support policy: patient_support.md

CHUNKING STRATEGIES EVALUATED:
    Fixed-size chunking
        Precision: 42.11%
        Recall: 100.00%
    Sentence-based chunking
        Precision: 42.11%
        Recall: 100.00%
    
    Chosen Strategy: Sentence-based chunking. 
        Both strategies achieved identical precision and recall on the evaluation set, sentence-based chunking was selected because
            - Chunks align with natural sentence boundaries
            - Retrieved passages are easier for users to interpret
            - Content fragmentation is reduced (fixed-size chunks truncated text towards the end which reduced coherence)
            - Knowledge-base updates produce more human-readable chunks
        Additionally, the purpose was not to prove which is the best strategy, rather to compare effectiveness and select most suitable strategy.
        The sentence-based collection (clinic_sentence_chunks) was used throughout Parts 2–4, including CrewAI retrieval, FastAPI deployment, AutoGen review, and dynamic document ingestion.

SIMILARITY THRESHOLD
    Created 10 queries (5 in-scope and 5 out-of-scope) and calculated distances. 
    Highest In-Scope Distance: 1.0128
    Lowest Out-of-Scope Distance: 1.7540
The threshold was selected between the two observed distance clusters and rounded to 1.4.

STRUCTURED OUTPUT VALIDATION
    All runtime assistant responses are validated against the CrewResponse pydantic schema before being returned by the API. Fields are:
        answer
        source
        confidence
        requires_escalation

FASTAPI DEPLOYMENT

HTTP Endpoints
    POST /ask Submit a healthcare support query.
    POST /add-document Dynamically add a new policy document.
    WebSocket Endpoint /chat
        Supports multi-turn conversations and handles client disconnects without terminating the server.

DYNAMIC DOCUMENT INGESTION
The deployment supports knowledge updated post-deployment. 

POST /add-document
{
  "doc_id": "zebra_policy_100",
  "text": "Zebra telehealth reviews are available only on Wednesday evenings."
}
Output:
{
  "message": "Document zebra_policy_100 added with 1 chunks"
}
---
POST /ask
Query:When are zebra telehealth reviews available?

Answer: Zebra telehealth reviews are available only on Wednesday evenings.
---
Result: PASS
The newly added policy was indexed into the active ChromaDB collection and subsequently retrieved through the policy search workflow.

SESSION MEMORY
LangChain session memory was implemented using InMemoryChatMessageHistory and RunnableWithMessageHistory.
Two demonstrations were completed:
    Multi-turn conversation showing context retained within a single session.
    Fresh-session conversation showing context correctly reset and unavailable.

GUARDRAILS

Input Guardrails
    Fixed-format contact number masking
    Prompt injection detection
    Output Guardrails

Groundedness validation against retrieved context
Unsupported questions return: "I don't know."
Demonstrations were completed for:
    Contact number masking
    Prompt injection blocking
    Groundedness rejection

AUTOGEN REVIEW STAGE
Two-agent RoundRobinGroupChat

Agents:
Policy Compliance Reviewer
Final Editor

Output:
VerdictModel
    The reviewer detects unsupported claims.
The editor either:
    approves the draft unchanged
    revises the draft by removing unsupported claims

MOCK_LLM Mode
    All evaluation and review workflows operate under a deterministic MOCK_LLM configuration. No external LLM API calls are required.
    Telemetry Disabled. CrewAI telemetry is disabled via: 
        CREWAI_DISABLE_TELEMETRY=true 
        OTEL_SDK_DISABLED=true


TASK 13: EVALUATION
15 queries were executed and evaluation was performed.
    Average Accuracy: 4.4
    Average Grounding: 5.0
    Average Completeness: 4.4
    Average Safety: 5.0
Detailed informaion is available in transcripts/task13_evaluation.txt

AI GOVERNANCE

Least Autonomy
    Only the Lookup Agent is permitted to invoke appointment lookup tools.

Risk Classification
    High Risk
    Reason: The system operates within the healthcare domain and processes appointment-related information.

Runtime Controls
    Token budget enforcement
    Response caching
    Structured logging

RESULTS SUMMARY:
    RAG System Evaluated
    CrewAI Multi-Agent Workflow
    Structured Outputs
    Guardrails
    FastAPI API
    WebSocket Endpoint
    AutoGen Review Team
    Runtime Governance
    Response Caching
    Dynamic KB Updates