# Practo Domain Support Agent

AI-powered healthcare support system built using CrewAI, RAG, FastAPI, and AutoGen.

## Project Goals

- Answer clinic policy questions using RAG
- Retrieve appointment information from structured records
- Support session-based memory
- Apply guardrails and governance controls
- Review responses using an AutoGen review team

## Current Progress

### Completed
- Deterministic appointment dataset generation
- Policy knowledge base creation

### In Progress
- Chunking strategies
- ChromaDB indexing
- Retrieval evaluation


## Retrieval Evaluation

Both chunking strategies were evaluated at the parent-document level. Retrieved chunks were mapped to their `document_id` values and duplicate document IDs were removed before calculating precision and recall.

The full evaluation output is available in:

- `transcripts/retrieval_metrics.txt`
- `transcripts/threshold_calibration.txt`

Run the evaluation with:

```bash
python retrieval_evaluation.py