import os, sys, re, json, io, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
WORK = os.path.join(HERE, "..", "out", "work07"); os.makedirs(WORK, exist_ok=True); os.chdir(WORK)
import scripted_api as api
from agent import ToolRegistry, run_agent
import tools
from tools import calculate, write_file, tool_specs, make_search_notes, SANDBOX

def last(path, events=("halt", "tool_call", "finish")):
    for line in open(path):
        r = json.loads(line)
        if r["event"] in events: print("   ", json.dumps(r)[:150])
base = tool_specs()
def pair_policy(messages, tools=None):   # one calculate per turn, forever (stand-in for a model that keeps going)
    n = api.n_assistant(messages); return "", [("calculate", {"expression": f"{n+1}+{n+1}"})]
def once(name, args):
    def p(messages, tools=None):
        return ("", [(name, args)]) if api.n_assistant(messages) == 0 else ("Done.", [])
    return p
def giveup(messages, tools=None): return "", [("calculate", {"expression": "1+1"})]

def final_text_policy(inner):
    def p(messages, tools=None):
        if messages and isinstance(messages[-1]["content"], str) and "run out of budget" in messages[-1]["content"]:
            return "I could not finish; stopped by a guardrail.", []
        return inner(messages, tools)
    return p

print("(a) iteration limit"); api.POLICY = final_text_policy(pair_policy)
reg = ToolRegistry(); reg.register("calculate", calculate, timeout=2.0)
run_agent("Compute 1+1 ... 8+8", reg, [base[0]], max_iterations=3, budget_usd=0.05, auto_approve=True, trace_path="g_a.jsonl", verbose=False); last("g_a.jsonl", ("halt",))
print("(b) budget limit (budget 0.004)")
run_agent("Compute 1+1 ...", reg, [base[0]], max_iterations=10, budget_usd=0.004, auto_approve=True, trace_path="g_b.jsonl", verbose=False); last("g_b.jsonl", ("halt",))
print("(b2) same, budget 0.0004")
run_agent("Compute 1+1 ...", reg, [base[0]], max_iterations=10, budget_usd=0.0004, auto_approve=True, trace_path="g_b2.jsonl", verbose=False); last("g_b2.jsonl", ("halt",))
print("(c) sandbox refusal"); api.POLICY = final_text_policy(once("write_file", {"filename": "../escape.md", "content": "hello"}))
reg2 = ToolRegistry(); reg2.register("write_file", write_file, timeout=5.0)
run_agent("Save hello to ../escape.md", reg2, [base[2]], max_iterations=3, budget_usd=0.05, auto_approve=True, trace_path="g_c.jsonl", verbose=False); last("g_c.jsonl", ("tool_call",))
print("(d) timeout")
def slow(seconds: int): time.sleep(seconds); return "done"
slow_spec = {"name": "slow", "description": "Sleep", "input_schema": {"type": "object", "properties": {"seconds": {"type": "integer"}}, "required": ["seconds"], "additionalProperties": False}}
api.POLICY = final_text_policy(once("slow", {"seconds": 8}))
reg3 = ToolRegistry(); reg3.register("slow", slow, timeout=2.0)
t0=time.time(); run_agent("Call slow with seconds=8.", reg3, [slow_spec], max_iterations=2, budget_usd=0.05, auto_approve=True, trace_path="g_d.jsonl", verbose=False); last("g_d.jsonl", ("tool_call",)); print("    wall-clock of run_agent:", round(time.time()-t0,2),"s (tool timeout 2.0 s; worker thread keeps sleeping)")
print("(e) unknown tool"); api.POLICY = final_text_policy(once("delete_everything", {}))
reg4 = ToolRegistry(); ghost={"name":"delete_everything","description":"x","input_schema":{"type":"object","properties":{},"additionalProperties":False}}
run_agent("Call delete_everything.", reg4, [ghost], max_iterations=2, budget_usd=0.05, auto_approve=True, trace_path="g_e.jsonl", verbose=False); last("g_e.jsonl", ("tool_call",))
print("(f) declined confirmation (stdin 'n')"); api.POLICY = final_text_policy(once("write_file", {"filename": "hello.md", "content": "hello"}))
sys.stdin = io.StringIO("n\n")
reg5 = ToolRegistry(); reg5.register("write_file", write_file, timeout=5.0, requires_confirmation=True)
run_agent("Save hello to hello.md", reg5, [base[2]], max_iterations=3, budget_usd=0.05, auto_approve=False, trace_path="g_f.jsonl", verbose=False); last("g_f.jsonl", ("tool_call",))
print("escape.md exists outside sandbox?", os.path.exists(os.path.join(SANDBOX.parent, "escape.md")), "| hello.md exists?", (SANDBOX/"hello.md").exists())

print("\n--- ex3 list_files")
def list_files() -> str:
    """Read-only listing of the sandbox root. Never recurses, never leaves."""
    entries = sorted(p for p in SANDBOX.iterdir() if p.is_file())
    if not entries:
        return "The sandbox is empty — no files have been saved yet."
    lines = [f"{p.name}\t{p.stat().st_size} bytes" for p in entries]
    total = sum(p.stat().st_size for p in entries)
    return "\n".join(lines) + f"\nTOTAL\t{total} bytes across {len(entries)} files"


LIST_FILES_SPEC = {
    "name": "list_files",
    "description": (
        "List the files already saved in the user's sandbox directory, with each "
        "file's size in bytes and a TOTAL line. Use this when the user asks what "
        "has been saved, what files exist, or how much space they take. Takes no "
        "arguments. It is read-only and cannot see anything outside the sandbox."
    ),
    "input_schema": {"type": "object", "properties": {}, "additionalProperties": False},
}

from agent import ToolRegistry
for f, body in [("costs.md","x"*62),("extraction-250.md","y"*74),("prompt-gain.md","z"*58)]: write_file(f, body)
def lf_policy(messages, tools=None):
    n = api.n_assistant(messages); res = api.tool_results(messages)
    if n == 0: return "Let me check the sandbox.", [("list_files", {})]
    if n == 1:
        tot = int(re.search(r"TOTAL\t(\d+) bytes", res[-1]).group(1)); return "", [("calculate", {"expression": f"{tot} / 1024"})]
    return "You have saved files totalling about 0.19 KB.", []
api.POLICY = lf_policy
registry = ToolRegistry(); registry.register("calculate", calculate, timeout=2.0)
registry.register("list_files", list_files, timeout=3.0)
run_agent("What files have you saved for me so far, and what is their total size in kilobytes?", registry, [base[0]] + [LIST_FILES_SPEC], max_iterations=6, budget_usd=0.05, auto_approve=True, trace_path="trace_list.jsonl")
