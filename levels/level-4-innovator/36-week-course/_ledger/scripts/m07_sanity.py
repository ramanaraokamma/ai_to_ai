from tools import calculate, write_file

print(calculate("0.00144 * 250"))        # 0.36
print(calculate("138 / 1117 * 100"))     # 12.3545219338
for bad in ["__import__('os').system('ls')", "138 merges / 1117", "2 ** 10 ** 10"]:
    try:
        calculate(bad)
    except Exception as e:
        print(f"{bad[:28]:30s} -> {type(e).__name__}: {e}")

for bad in ["../escape.md", "/etc/passwd", "run.sh"]:
    try:
        write_file(bad, "x")
    except Exception as e:
        print(f"{bad:15s} -> {type(e).__name__}")

