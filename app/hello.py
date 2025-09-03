import os, socket, time, pathlib

def main():
    mount = os.environ.get("DATA_DIR", "/data")
    p = pathlib.Path(mount) / "hello.txt"
    print("[hello] starting")
    print(f"[hello] hostname: {socket.gethostname()}")
    print(f"[hello] writing to: {p}")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("hello kubeflow!\n", encoding="utf-8")
    print("[hello] wrote /data/hello.txt")
    # sleep a little so you can see logs
    time.sleep(2)

if __name__ == "__main__":
    main()
