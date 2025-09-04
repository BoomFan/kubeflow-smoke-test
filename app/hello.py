import os, socket, time
from pathlib import Path

def main():
    # Write outputs to the launch directory (mounted by trainjob.py)
    out_dir = os.environ.get("OUT_DIR", ".")
    p = Path(out_dir) / "hello.txt"
    print("[hello] starting")
    print(f"[hello] hostname: {socket.gethostname()}")
    print(f"[hello] writing to: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("hello kubeflow (trainjob.py)!\n", encoding="utf-8")
    print("[hello] wrote", p)
    time.sleep(1)

if __name__ == "__main__":
    main()
