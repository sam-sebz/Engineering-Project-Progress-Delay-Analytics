# Engineering Project Progress and Delay Monitoring System

Full local prototype for tracking engineering-project progress and estimating activity delay risk.

## Included
- Project and activity management
- Progress aggregation
- ML delay-risk prediction
- FastAPI backend
- SQLite persistence
- Browser dashboard
- Reproducible training script
- PRD, TRD, project flow, UI UX design, backend schema and implementation plan

## Measured result
- 250 simulated projects
- 3000 activity records
- 0.803 ROC AUC
- 74.83 percent accuracy
- 66.96 percent F1 score

## Run
```bash
pip install -r requirements.txt
python src/train_model.py
uvicorn src.main:app --reload --port 8003
```

Open http://127.0.0.1:8003

Note: all project and training data is synthetic or simulated.
