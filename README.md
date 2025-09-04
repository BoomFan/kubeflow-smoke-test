# Kubeflow Smoke Test (Tiny Project)

A **minimal** smoke test project for Kubeflow environments that use the trainjob.py submit workflow.
This project helps verify that:

- Your experiment directory under `/home_bu/...` is correctly mounted into the worker container.

- Python runs inside the container image you specify.

- Logs are visible through trainjob.py logs.

- Output files written by your script appear in your experiment directory on the head node.

## Files
- `app/hello.py` — a tiny Python program that prints a few log lines and writes `hello.txt`

- `run_smoke.sh` — a launcher script; you will pass this to `trainjob.py` --cmd

---

## Step-by-step

### 0)Copy a laptop local path to the Kubeflow Cluster

make sure from another terminal, connect to cluster using:
```bash
ssh -i ~/.ssh/id_rsa -p 2222 jovyan@localhost
```

and then copy by scp:

```bash
scp -P 2222 -i ~/.ssh/id_rsa -r /Users/fabu/FanBu/kubeflow-smoke-test jovyan@localhost:/home/jovyan/fabu/
```


### 1) Choose your experiment name (follow your team’s naming convention)

```bash
cd ~/fabu/kubeflow-smoke-test
export USER_NAME=fb
export EXP_NAME=smoke_y25w36_fb01
export EXP_DIR=~/fabu/FanBu/Output/$USER_NAME/sft/$EXP_NAME
```

### 2) Create the experiment directory and copy the project files
```bash
mkdir -p "$EXP_DIR"
rsync -av --exclude="$EXP_DIR" ./ "$EXP_DIR/"
```

### 3) Run the Job
```bash
cd "$EXP_DIR"
chmod +x run_smoke.sh

IMAGE="https://containers.cisco.com/papyrus_ai/simple-sudo:jasmacka-v0.0.4"

trainjob.py submit \
  --name ${USER_NAME}-smoke-01 \
  --cpu 1 \
  --memory 2Gi \
  --nnodes 1 \
  --nproc-per-node 1 \
  --cmd "bash $EXP_DIR/run_smoke.sh" \
  --container-image "$IMAGE"
```
- `--name` must be globally unique (otherwise you may attach to someone else’s old job).

- `--container-image` should be a Python-capable image available in your cluster.

### 4) Verify the output file 
When running the job
```bash
ktrainjob.py list
trainjob.py logs ${USER_NAME}-smoke-01
```
After the job finishes, check your experiment directory:
```bash
ls -l "$EXP_DIR"
cat "$EXP_DIR/hello.txt"
```

---

## Expected Results
Logs should contain:
```bash
[hello] starting
[hello] writing to: /home_bu/.../hello.txt
[hello] wrote /home_bu/.../hello.txt
[run] done
```
And a file `hello.txt` with:
```bash
hello kubeflow (trainjob.py)!
```