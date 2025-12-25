# Mem0 Stack Setup Guide (AWS-first)

Start here: [`README.md`](README.md) • Next: [`api.md`](api.md)

Deploy a self-hosted AI memory API on AWS using:

- FastAPI + Mem0
- Qdrant (vector DB)
- AWS Bedrock: Titan embeddings + a Bedrock LLM

---

## Path A (Recommended): Terraform + AWS Bedrock

This is the default for the lab: one `terraform apply` provisions the AWS resources and boots the containers.

### Prereqs (your laptop)

- AWS credentials configured (AWS CLI / SSO / assumed role)
- Terraform installed
- Bedrock enabled in your AWS region and **model access granted**

### Deploy

From repo root:

```bash
cd infra/terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply
```

Note: after `terraform apply`, the instance boots via `user_data` and the API may take **a few minutes** before `swagger_url` is reachable.

### Get URLs + keys (for Swagger)

```bash
cd infra/terraform
terraform output -raw swagger_url
terraform output -raw api_base_url
terraform output -raw api_key
terraform output -raw admin_api_key
```

### Use Swagger (this is the lab)

- Open the Swagger URL from Terraform output: `terraform output -raw swagger_url`
- Click **Authorize**
- Paste:
  - `terraform output -raw api_key` into **X-API-Key**
  - `terraform output -raw admin_api_key` into **X-Admin-Key**

Then run:

- `POST /v1/demo/seed/tony-stark`
- `POST /v1/demo/seed/leia-organa`
- `POST /v1/demo/seed/hermione-granger`

---

## Optional Provider Track: OpenAI

If you want to use OpenAI instead of Bedrock, set in `.env`:

- `LLM_PROVIDER=openai`
- `EMBEDDER_PROVIDER=openai`
- `OPENAI_API_KEY=...`

Everything else stays the same.

---

## Debugging `infer=true` (Bedrock)

If you see `{"results":[]}` when calling `/v1/memories/add` with `infer=true`, enable Mem0's Bedrock LLM debug logging:

- Set `MEM0_DEBUG_LLM=1` in the API container environment (Terraform writes `.env` on the instance)
- Then check logs:

```bash
sudo docker logs mem0_api --tail 200
```

You should see `[MEM0_DEBUG_LLM]` lines showing the raw model response so you can confirm whether it returned valid JSON facts.

---

Next: [`api.md`](api.md)
