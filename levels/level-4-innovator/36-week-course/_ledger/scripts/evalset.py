"""FROZEN EVAL SET — written 2026-09-01, before any training. Do not edit.
Each case: (text, gold_label, category). Category == label here, but keep the
column: on other tasks you will want categories that cut across labels."""

LABELS = ["greeting", "refund", "technical", "billing", "out_of_scope"]

EVAL = [
    # ---- greeting (6) ----
    ("hey! quick one for you",                                  "greeting"),
    ("good afternoon, are you there?",                          "greeting"),
    ("hiya",                                                    "greeting"),
    ("hello - first time using this",                           "greeting"),
    ("morning, got a sec?",                                     "greeting"),
    ("hi, hope this is the right place",                        "greeting"),
    # ---- refund (7) ----
    ("these shoes are the wrong colour, how do I send them back?", "refund"),
    ("I'd like my money returned for order 55301",              "refund"),
    ("is there a time limit on sending items back?",            "refund"),
    ("package never arrived, I want reimbursing",               "refund"),
    ("do I pay postage to return something?",                   "refund"),
    ("cancel order 7781 and put the money back on my card",     "refund"),
    ("opened it, hated it - can I still send it back?",         "refund"),
    # ---- technical (7) ----
    ("clicking save does absolutely nothing",                   "technical"),
    ("everything is blank after I sign in",                     "technical"),
    ("the android version force closes on launch",              "technical"),
    ("my csv download has headers but no rows",                 "technical"),
    ("reset email never turns up in my inbox",                  "technical"),
    ("charts stopped rendering yesterday afternoon",            "technical"),
    ("keeps saying 'network error' on a perfect connection",    "technical"),
    # ---- billing (5) ----
    ("took the money twice on the 3rd",                         "billing"),
    ("swap me onto the yearly plan",                            "billing"),
    ("need a proper tax invoice for accounting",                "billing"),
    ("what am I paying per month right now?",                   "billing"),
    ("card expired, where do I put the new one?",               "billing"),
    # ---- out_of_scope (5) ----
    ("what's a good recipe for dosa?",                          "out_of_scope"),
    ("how tall is Mount Kilimanjaro?",                          "out_of_scope"),
    ("write my sister a birthday message",                      "out_of_scope"),
    ("explain quantum entanglement",                            "out_of_scope"),
    ("should I buy bitcoin?",                                   "out_of_scope"),
]

assert len(EVAL) == 30

