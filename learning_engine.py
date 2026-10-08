from ml_model import recommend

def context_from_status(status_df):
    weak=status_df[status_df.status=="Needs Practice"].topic.tolist()
    strong=status_df[status_df.status=="Mastered"].topic.tolist()
    return f"Weak topics: {', '.join(weak) or 'none'}. Mastered topics: {', '.join(strong) or 'none'}."

def next_step(status_df):
    return recommend(status_df)
