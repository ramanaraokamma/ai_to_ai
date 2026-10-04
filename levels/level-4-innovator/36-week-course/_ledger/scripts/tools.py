"""Three tools, each with its own guardrails. Tools raise; the agent catches."""
import ast
import json
import operator
from pathlib import Path

# ------------------------------------------------------------------ sandbox
SANDBOX = Path("agent_sandbox").resolve()  # relative to cwd
SANDBOX.mkdir(exist_ok=True)
ALLOWED_SUFFIXES = {".md", ".txt", ".json"}
MAX_FILE_BYTES = 20_000


# --------------------------------------------------------------- calculator
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
}


def _eval_node(node):
    """Walk a parsed expression tree. Anything not explicitly allowed is refused."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise ValueError(f"only numeric literals are allowed, got {node.value!r}")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left, right = _eval_node(node.left), _eval_node(node.right)
        # Guardrail: 2 ** 10 ** 10 would hang the process for hours.
        if isinstance(node.op, ast.Pow) and (abs(right) > 64 or abs(left) > 1e6):
            raise ValueError("exponent too large; keep ** small")
        return _OPS[type(node.op)](left, right)
    raise ValueError(f"unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> str:
    """Evaluate arithmetic safely. Never uses eval()."""
    if not isinstance(expression, str):
        raise ValueError("expression must be a string")
    if len(expression) > 200:
        raise ValueError("expression too long (max 200 characters)")
    tree = ast.parse(expression, mode="eval")     # SyntaxError -> caught by caller
    value = _eval_node(tree)
    return repr(round(value, 10) if isinstance(value, float) else value)


# ------------------------------------------------------------- notes search
def make_search_notes(index, titles):
    """Close over a Module 6 VectorIndex and return a callable tool."""

    def search_notes(query: str, k: int = 3) -> str:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        k = max(1, min(int(k), 5))                # clamp, don't trust
        hits = index.search(query, k=k)
        if not hits or hits[0][1] < 0.05:
            return "NO_RELEVANT_NOTES (best similarity below 0.05)"
        lines = []
        for cid, sim, text in hits:
            if sim < 0.05:
                continue
            body = text.split("\n", 1)[1].strip() if "\n" in text else text
            lines.append(f"[note {cid}] (similarity {sim:.3f}) {titles[cid]}\n{body}")
        return "\n\n".join(lines)

    return search_notes


# --------------------------------------------------------------- write file
def write_file(filename: str, content: str) -> str:
    """Write inside SANDBOX only. Resolve first, compare second."""
    if not isinstance(filename, str) or not filename.strip():
        raise ValueError("filename must be a non-empty string")
    target = (SANDBOX / filename).resolve()       # collapses .. and follows symlinks

    if not target.is_relative_to(SANDBOX):
        raise PermissionError(
            f"refused: '{filename}' resolves to {target}, outside the sandbox "
            f"{SANDBOX}. Only flat filenames at the sandbox root are allowed."
        )
    if target.suffix.lower() not in ALLOWED_SUFFIXES:
        raise PermissionError(
            f"refused: suffix '{target.suffix}' not allowed. "
            f"Use one of {sorted(ALLOWED_SUFFIXES)}."
        )
    if not target.parent.exists():
        raise ValueError(
            f"directory '{Path(filename).parent}' does not exist in the sandbox. "
            f"Write to a flat filename at the sandbox root, e.g. 'report.md'."
        )
    data = content.encode("utf-8")
    if len(data) > MAX_FILE_BYTES:
        raise ValueError(f"content too large: {len(data)} bytes > {MAX_FILE_BYTES}")
    target.write_bytes(data)
    return f"wrote {len(data)} bytes to {target.name}"


# -------------------------------------------------------- schemas for the API
def tool_specs():
    return [
        {
            "name": "calculate",
            "description": (
                "Evaluate a single arithmetic expression and return the number. "
                "Supports + - * / // % ** and parentheses over numeric literals only. "
                "Use this for EVERY calculation, including simple ones — do not do "
                "arithmetic in your head. Do NOT pass words, units, or variable names: "
                "'138 / 1117 * 100' is valid, '138 merges / 1117 bytes' is not."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic over digits only, e.g. '0.00144 * 250'.",
                    }
                },
                "required": ["expression"],
                "additionalProperties": False,
            },
        },
        {
            "name": "search_notes",
            "description": (
                "Search the user's personal AI lab notebook and return the top matching "
                "entries, each with a note id and a similarity score. Use this for ANY "
                "question about what the user did, measured, configured, or concluded in "
                "their own experiments. Returns the literal string NO_RELEVANT_NOTES when "
                "nothing matches — when you see that, say the notebook does not cover it "
                "instead of answering from general knowledge. Do NOT use this for public "
                "facts or for arithmetic."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "A natural-language search query.",
                    },
                    "k": {
                        "type": "integer",
                        "description": "How many notes to return, 1-5. Default 3.",
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "name": "write_file",
            "description": (
                "Save text to a file in the user's sandbox directory. Use ONLY when the "
                "user explicitly asked for something to be saved or written to a file. "
                "Filenames must be flat (no directories, no '..' , no leading '/') and end "
                "in .md, .txt or .json. Writing requires human approval, so call it once "
                "with the final content — do not call it to test whether it works."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Flat filename, e.g. 'costs.md'.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full text to write.",
                    },
                },
                "required": ["filename", "content"],
                "additionalProperties": False,
            },
        },
    ]

