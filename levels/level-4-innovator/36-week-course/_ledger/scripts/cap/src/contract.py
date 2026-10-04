"""The answer contract. One definition, five consumers, no drift."""
from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

VERSION = "v1"
LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "trace.jsonl"
MAX_LOGGED_CHARS = 400          # a privacy decision — justify it in S6


@dataclass
class Answer:
    question: str
    route: str                       # retrieve | agent | refuse | trained_model
    text: str
    refused: bool = False
    citations: list[int] = field(default_factory=list)
    retrieved_ids: list[int] = field(default_factory=list)
    top_similarity: float = 0.0
    iterations: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    version: str = VERSION
    request_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z")

    def citations_valid(self) -> bool:
        """Rule 3, mechanically. Every cited id must have actually been retrieved."""
        return all(c in self.retrieved_ids for c in self.citations)


def log_answer(ans: Answer, **extra) -> None:
    """Append one JSON object on one line. Append-only, never rewritten."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(ans)
    row["question"] = row["question"][:MAX_LOGGED_CHARS]
    row["text"] = row["text"][:MAX_LOGGED_CHARS]
    row["question_chars"] = len(ans.question)     # keep the true length
    row.update(extra)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")

