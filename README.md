# Local DevOps Store

Local learning MVP: storefront, Nginx, product/order APIs, simulated payment service, PostgreSQL.

## Run

From WSL, open this folder (keep project files in the Linux filesystem for best performance), then run:

```bash
docker compose up --build -d
```

Open http://localhost:8088. Add products and check out with `demo-ok`. Use token `fail` to simulate a declined payment. API docs are available on each internal service; from the browser try `/api/products`. Watch logs with `docker compose logs -f`; stop with `docker compose down`.

To reset all database content and re-seed sample products, run `docker compose down -v` and then start again. This deletes the local database volume.

## Project layout

- `web/` storefront and Nginx routing
- `services/products/` catalog API
- `services/orders/` order API and persistence
- `services/payments/` safe local payment simulator
- `database/init.sql` schema and sample catalog
- `docker-compose.yml` local application stack

## End-to-end path

1. Make a UI change, then rebuild with `docker compose up --build -d web`.
2. Push this folder to GitHub and add a GitHub Actions workflow to build/test on pull requests.
3. Enable Kubernetes in Docker Desktop. Add Deployments and Services for each service; expose the web frontend locally.
4. Install Argo CD in that cluster. Put Kubernetes manifests in Git and point Argo CD at them; change a manifest and watch it sync.
5. Add Jenkins as a second CI exercise once Actions works. Have it run the same checks/build; use one active deployment path while learning.
6. Add logs, metrics, database backup/restore, and practice debugging and rollback.

## Scope and safety

This is an educational local MVP, not production commerce software. It omits authentication, stock locking, refunds, and robust payment reconciliation. The payment service generates a fake payment ID and does not process or store card details. The database password is local-only. The services share one database for learning simplicity; production microservices should own independent data and coordinate workflows reliably.
