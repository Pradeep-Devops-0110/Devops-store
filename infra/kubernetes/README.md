# Local Kubernetes layout

This project uses one local Kubernetes cluster with separate namespaces:

- `devtools`: Jenkins, Argo CD, Prometheus, and Grafana.
- `app-dev`: storefront, Nginx, backend services, and PostgreSQL.

Create the namespaces after enabling Kubernetes in Docker Desktop:

```bash
kubectl apply -f infra/kubernetes/namespaces/
kubectl get namespaces
```

Keep deployment manifests for the store under `infra/kubernetes/app-dev/`. Install platform tools into `devtools` using their supported charts or manifests. Argo CD will run in `devtools` and be configured to deploy the application into `app-dev`.

For a small local machine, install the platform components in stages. Start with Argo CD, then Jenkins, then monitoring. The namespace separates names and access policies, but all components still share the machine's CPU and memory. Use persistent storage for Jenkins and Grafana data if you want it to survive restarts.
