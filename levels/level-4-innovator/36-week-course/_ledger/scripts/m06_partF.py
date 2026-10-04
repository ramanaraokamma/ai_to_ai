from m06_lib import *
TEST_QUESTIONS = ANSWERABLE[:8] + UNANSWERABLE[:2]
total_cost = 0.0
for q in TEST_QUESTIONS:
    print(f"\nQ: {q}")
    r = ask(index, q)
    total_cost += r["in_tok"] / 1e6 * 2.00 + r["out_tok"] / 1e6 * 10.00
    print(f"  A: {r['answer']}")
    print(f"     cited={r['cited']} served={r['served']} "
          f"sim={r['best_sim']:.3f} refused_by={r['refused_by']}")
print(f"\ntotal cost for {len(TEST_QUESTIONS)} questions: ${total_cost:.4f}")

