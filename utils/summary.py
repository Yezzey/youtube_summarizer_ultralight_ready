from transformers import pipeline

summarizer = pipeline("summarization", model="csebuetnlp/mT5_small_finetuned_summarize_news")

def summarize_text(text):
    chunks = [text[i:i+1024] for i in range(0, len(text), 1024)]
    summarized = [summarizer(chunk, max_length=60, min_length=20, do_sample=False)[0]["summary_text"] for chunk in chunks]
    return " ".join(summarized)