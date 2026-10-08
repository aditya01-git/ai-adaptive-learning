import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

LABELS = {0:"Needs Practice", 1:"Improving", 2:"Mastered"}
FEATURES = ["latest_pct","avg_pct","attempts","trend","coding_score"]

def train_model():
    rng = np.random.default_rng(42)
    rows, labels = [], []
    for _ in range(900):
        latest = rng.uniform(20,100)
        avg = np.clip(latest + rng.normal(0,12), 0, 100)
        attempts = int(rng.integers(1,9))
        trend = latest - avg
        coding = np.clip(avg + rng.normal(0,15), 0, 100)
        if avg < 55 or (latest < 60 and trend < 0):
            label = 0
        elif avg >= 78 and latest >= 75 and coding >= 65:
            label = 2
        else:
            label = 1
        rows.append([latest,avg,attempts,trend,coding]); labels.append(label)
    model = RandomForestClassifier(n_estimators=80,max_depth=5,random_state=42)
    return model.fit(pd.DataFrame(rows,columns=FEATURES),labels)

def build_features(quizzes, coding, topics):
    out=[]
    for topic in topics:
        q = quizzes[quizzes.topic==topic] if not quizzes.empty else pd.DataFrame()
        c = coding[coding.topic==topic] if not coding.empty else pd.DataFrame()
        if q.empty:
            out.append({"topic":topic,"latest_pct":0,"avg_pct":0,"attempts":0,"trend":0,
                        "coding_score":float(c.score.mean()) if not c.empty else 0})
            continue
        latest=float(q.iloc[-1].pct); avg=float(q.pct.mean())
        code=float(c.score.mean()) if not c.empty else avg
        out.append({"topic":topic,"latest_pct":latest,"avg_pct":avg,
                    "attempts":len(q),"trend":latest-avg,"coding_score":code})
    return pd.DataFrame(out)

def classify(model, quizzes, coding, topics):
    feats=build_features(quizzes,coding,topics)
    X=feats[FEATURES]
    pred=model.predict(X)
    probs=model.predict_proba(X).max(axis=1)
    feats["status"]=[LABELS[int(x)] if r.attempts else "Not Started"
                     for x,r in zip(pred,feats.itertuples())]
    feats["confidence"]=np.where(feats.attempts>0,probs,1.0)
    return feats

def recommend(status_df):
    active=status_df[status_df.status!="Not Started"]
    weak=active[active.status=="Needs Practice"].sort_values(["avg_pct","latest_pct"])
    if not weak.empty:
        r=weak.iloc[0]
        return r.topic, f"{r.topic} is currently your biggest opportunity. Practice it before moving ahead."
    improving=active[active.status=="Improving"].sort_values("avg_pct")
    if not improving.empty:
        r=improving.iloc[0]
        return r.topic, f"{r.topic} is improving. One more focused practice round should strengthen it."
    new=status_df[status_df.status=="Not Started"]
    if not new.empty:
        return new.iloc[0].topic, f"{new.iloc[0].topic} is next in your learning path."
    return None, "Excellent work. You have mastered the current path. Try another language or a challenge."
