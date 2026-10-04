PRICE_IN_PER_MTOK = 2.00     # Claude Sonnet 5, USD per 1M input tokens
PRICE_OUT_PER_MTOK = 10.00   # USD per 1M output tokens

def cost(input_tokens, output_tokens):
    return (input_tokens / 1e6) * PRICE_IN_PER_MTOK + \
           (output_tokens / 1e6) * PRICE_OUT_PER_MTOK

print(f"one call  (12,000 in / 800 out): ${cost(12_000, 800):.4f}")
print(f"1,000 such calls               : ${cost(12_000, 800) * 1000:.2f}")

BUDGET = 5.00
print(f"calls affordable on ${BUDGET:.2f}: {int(BUDGET / cost(12_000, 800))}")
