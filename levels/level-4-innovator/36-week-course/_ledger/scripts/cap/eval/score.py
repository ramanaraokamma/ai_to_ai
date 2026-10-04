# eval/score.py
def score_case(case, ans):
    """Return (passed: bool, reason: str). No partial credit at this level —
    partial credit hides the fact that half an answer is often useless."""
    if case["must_refuse"]:
        if ans.refused:
            return True, "correctly refused"
        return False, f"should have refused, said: {ans.text[:60]!r}"

    if ans.refused:
        return False, "refused an answerable question"

    low = ans.text.lower()
    needles = [n.lower() for n in case["must_contain"]]
    hit = any(n in low for n in needles) if case.get("any_of") else \
          all(n in low for n in needles)
    if not hit:
        missing = [n for n in needles if n not in low]
        return False, f"missing {missing}"

    if case["must_cite"]:
        if not ans.citations:
            return False, "no citation"
        stray = [c for c in ans.citations if c not in ans.retrieved_ids]
        if stray:
            return False, f"cited chunks that were never retrieved: {stray}"

    return True, "ok"

