from pathlib import Path
import json,joblib
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/"artifacts"; ART.mkdir(exist_ok=True)
(ROOT/"data").mkdir(exist_ok=True)

rng=np.random.default_rng(2026)
projects=250
activities_per_project=12
rows=[]

for pid in range(1,projects+1):
    for a in range(activities_per_project):
        planned=int(rng.integers(5,31))
        progress=float(np.clip(rng.normal(.65,.25),.05,1))
        risk=float(rng.normal(0,1))
        delay=int(max(0,rng.normal(2+10*(1-progress)+3*risk,4)))
        rows.append([pid,a+1,planned,progress,risk,delay,int(delay>=7)])

df=pd.DataFrame(rows,columns=["project_id","activity_no","planned_days","progress","risk_signal","delay_days","delayed"])
X=df[["planned_days","progress","risk_signal"]]
y=df["delayed"]

Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.20,random_state=42,stratify=y)
model=Pipeline([("scale",StandardScaler()),("m",LogisticRegression(max_iter=2000,random_state=42))])
model.fit(Xtr,ytr)
pred=model.predict(Xte)
score=model.predict_proba(Xte)[:,1]

metrics={
 "projects":projects,
 "activities":len(df),
 "accuracy":float(accuracy_score(yte,pred)),
 "precision":float(precision_score(yte,pred)),
 "recall":float(recall_score(yte,pred)),
 "f1":float(f1_score(yte,pred)),
 "roc_auc":float(roc_auc_score(yte,score))
}

df.to_csv(ROOT/"data"/"project_activities.csv",index=False)
(ART/"metrics.json").write_text(json.dumps(metrics,indent=2))
joblib.dump(model,ART/"delay_model.joblib")
print(json.dumps(metrics,indent=2))
