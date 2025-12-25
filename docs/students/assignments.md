# Assignments (After the Lab)

Prev: [`api.md`](api.md) • Optional reading: [`architecture.md`](architecture.md)

Students must complete the **Required** section (in order), then pick **any 2** from the **Optional** section.

## Required (do these in order)

1. **Separate API key vs Admin key (Terraform)**
   - Update Terraform so it generates **two distinct keys by default**:
     - `api_key` (for `/v1/*`)
     - `admin_api_key` (for `/admin/*`)
   - Use `random_password` (same approach as the existing `api_key`) and write both values to SSM so the instance bootstraps correctly.
   - Acceptance criteria:
     - Terraform outputs show **two different values**
     - Swagger works when you set:
       - `X-API-Key` = `terraform output -raw api_key`
       - `X-Admin-Key` = `terraform output -raw admin_api_key`

2. **Rotate API keys (new endpoint + Swagger testing)**
   - Create an **admin-only** endpoint:
     - Suggested shape: `POST /admin/keys/rotate` (requires `X-Admin-Key`)
   - Requirements:
     - returns the new key(s) in the response
     - after rotation, old keys should no longer work
     - update docs with how to use it from Swagger
   - Design choice (explain tradeoffs):
     - **Easy mode**: rotate keys in-memory (works until container restarts)
     - **Real mode**: write new key(s) to **SSM Parameter Store** and restart/reload the API so it takes effect

---

## Optional (pick any 2)

### 1) Monitoring (Qdrant → CloudWatch dashboard)

- Send Qdrant metrics to **CloudWatch** and build a dashboard.
- Make it “vector DB-specific” (not just CPU/RAM): things like collection size / point count growth, search request latency, and index behavior.
- Implementation hint: Qdrant exposes Prometheus-style metrics; scrape them and publish to CloudWatch (multiple valid AWS approaches).

### 2) Explore the Qdrant dashboard (port 6333)

Goal: learn what Qdrant stores and what “a vector database” looks like in practice.

- **Recommended (safe)**: use SSH port forwarding, then open the dashboard locally:
  - `ssh -i <your-key.pem> -L 6333:localhost:6333 ec2-user@<EC2_PUBLIC_IP>`
  - Open: `http://localhost:6333/dashboard`
- **Alternate (less safe)**: set `expose_qdrant_public = true` in Terraform (this opens port 6333 to the internet).

What to do in the dashboard:

- Find the `mem0` collection and inspect stored points/payloads (what fields exist? where is `user_id`?).
- Compare “raw memories” (`infer=false`) vs “extracted facts” (`infer=true`) by looking at the text stored.
- Notice how “search” is vector-based (semantic) vs keyword-based (exact match).

How to improve it (design ideas):

- Make access safer (do not expose 6333 publicly; keep SSH tunneling or add auth/reverse proxy).
- Add dashboard notes/screenshots to the lab docs (what students should look for).
- (Stretch) Pin the Qdrant image tag for repeatable classroom behavior.

### 3) API / Swagger refactor

- Add a new endpoint or refactor request/response shapes and update docs.

### 4) Data-minded extension

- Export `/admin/all-memories` results to CSV and build a small analysis notebook (topics, per-user counts, growth over time).

### Bonus (does not count toward the “pick any 2”)

- **SSM-first secrets**: move any secrets out of `terraform.tfvars` and into SSM created out-of-band, then modify Terraform to read them.


