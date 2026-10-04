import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, "src")); sys.path.insert(0, os.path.join(HERE, "eval")); sys.path.insert(0, os.path.join(HERE, ".."))
sys.argv = ["run_eval.py"]
src = open("eval/run_eval.py").read().replace("sys.path.insert(0, str(Path(__file__).resolve().parent.parent / \"src\"))", "")
exec(compile(src, "run_eval.py", "exec"))
