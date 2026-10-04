import stub_anthropic as anthropic
from m05_prompts import *
from bench import TESTS, run_suite, report, field_breakdown

MODEL = "claude-sonnet-5"
client = anthropic.Anthropic()

SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "category": {"type": "string",
                         "enum": ["billing", "shipping", "technical", "account", "other"]},
            "urgency": {"type": "integer", "enum": [1, 2, 3]},
            "order_id": {"type": ["string", "null"]},
            "refund_requested": {"type": "boolean"},
        },
        "required": ["category", "urgency", "order_id", "refund_requested"],
        "additionalProperties": False,
    },
}


def make_caller(version, guard):
    cfg = PROMPTS[version]

    def call(text):
        kwargs = dict(
            model=MODEL,
            max_tokens=300,
            system=cfg["system"],
            messages=[{"role": "user",
                       "content": cfg["template"].replace("{{TEXT}}", text)}],
        )
        if cfg["schema"]:
            kwargs["output_config"] = {"format": SCHEMA}

        try:
            r = client.messages.create(**kwargs)
        except anthropic.BadRequestError as e:
            raise RuntimeError(f"bad request for {version}: {e.message}") from e
        except anthropic.RateLimitError:
            time.sleep(5)
            r = client.messages.create(**kwargs)     # one retry; SDK also retries internally

        if r.stop_reason == "max_tokens":
            print(f"  ⚠️  {version}: output truncated — raise max_tokens")

        text_out = "".join(b.text for b in r.content if b.type == "text")
        guard.record(r.usage.input_tokens, r.usage.output_tokens)
        return text_out, r.usage.input_tokens, r.usage.output_tokens

    return call


