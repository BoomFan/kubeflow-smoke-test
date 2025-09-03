# Kubeflow Smoke Test (Tiny Project)

A **minimal** project to prove you can run a containerized Python script on your Kubeflow cluster (no external network required).

## What it does
- Runs a tiny Python script that prints logs and writes `/data/hello.txt` into a PVC.
- Lets you verify: image pull, env injection, volume mount, logs, and output artifact.

## Files
- `Dockerfile` – build a tiny Python image
- `app/hello.py` – prints logs and writes a file
- `k8s/pvc.yaml` – 5Gi PVC (adjust storage class if needed)
- `k8s/job.yaml` – a one-off K8s Job to run the script in your Kubeflow namespace

> **No Secrets needed**. This example avoids OpenAI/network calls on purpose.

---

## Step-by-step

### 1) Build & push image
Replace `<REGISTRY>` with your container registry (e.g., `gcr.io/your-proj`, `ghcr.io/yourname`, `harbor.company.io/yourproj`).

```bash
docker build -t <REGISTRY>/kubeflow-smoke-test:latest .
docker push <REGISTRY>/kubeflow-smoke-test:latest
```

### 2) Create PVC
```bash
kubectl apply -f k8s/pvc.yaml
```

If your cluster requires a storageClass, add:
```yaml
spec:
  storageClassName: <your-storage-class>
```

### 3) Run the Job
Edit `k8s/job.yaml` to set your image (`<REGISTRY>/kubeflow-smoke-test:latest`), then:
```bash
kubectl apply -f k8s/job.yaml
kubectl logs -f job/kf-smoke-job
```

You should see logs ending with:
```
[hello] wrote /data/hello.txt
```

### 4) Verify the output file in the PVC
Start a temporary pod that mounts the same PVC and check the file:
```bash
kubectl run pvc-inspect --image=busybox -i --restart=Never --overrides='{
  "spec": {
    "volumes": [{"name": "ws", "persistentVolumeClaim": {"claimName": "kf-smoke-pvc"}}],
    "containers": [{
      "name": "busy",
      "image": "busybox",
      "command": ["sh","-c","sleep 3600"],
      "volumeMounts": [{"name":"ws","mountPath":"/data"}]
    }]
  }
}'
kubectl exec -it pvc-inspect -- sh -lc 'ls -l /data && echo "---" && cat /data/hello.txt'
kubectl delete pod pvc-inspect
```

If you see the file content, your Kubeflow environment is wired up correctly.

---

## Troubleshooting

- **ImagePullBackOff**: Ensure your cluster can pull from your registry (configure ImagePullSecret if private).
- **Pending PVC**: Your namespace may need a specific `storageClassName`. Ask your cluster admin.
- **Job not found/logs empty**: Make sure you’re in the **right namespace** (Kubeflow often isolates users). Use `-n <ns>` on kubectl commands.
- **Permission issues**: Check PodSecurity/NetworkPolicies; this example doesn’t need egress.

Once this works, you can switch the Job’s command to run your real TripletForge scripts.
