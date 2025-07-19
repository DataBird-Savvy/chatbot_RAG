from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# Ground truth and response
reference = "Products are eligible for return within 30 days if unused and in original packaging."
candidate = ("The return policy for TechEase Solutions states that products are eligible for return "
             "within 30 days, provided they are unused and in their original packaging. This means "
             "you need to make sure the item hasn't been used and the packaging is intact to qualify "
             "for a return. If you need more details or assistance with a return, feel free to ask!")

# BLEU Score (use smoothing for short sentences)
reference_tokens = [reference.split()]
candidate_tokens = candidate.split()
bleu_score = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=SmoothingFunction().method1)

# ROUGE Score
scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
rouge_scores = scorer.score(reference, candidate)

# Output
print(f"BLEU Score: {bleu_score:.4f}")
print("ROUGE Scores:")
for k, v in rouge_scores.items():
    print(f"  {k}: Precision={v.precision:.4f}, Recall={v.recall:.4f}, F1={v.fmeasure:.4f}")
