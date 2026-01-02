# Team Assignments

Prev: [`api.md`](api.md) • Optional reading: [`architecture.md`](architecture.md)

**Note:** The in-class lab is **individual work**. These assignments are **team-based** (3-4 students per team).

---

## Part 1: Individual Assignments

Complete these on your own deployment:

### 1. Separate API key vs Admin key (Terraform)

Update Terraform to generate **two distinct keys by default**:

- `api_key` (for `/v1/*` endpoints)
- `admin_api_key` (for `/admin/*` endpoints)

Use `random_password` (same approach as existing `api_key`) and write both values to SSM.

**Acceptance criteria:**

- `terraform output` shows two different keys
- Swagger works with `X-API-Key` and `X-Admin-Key` headers

### 2. Rotate API keys (new endpoint)

Create an **admin-only** endpoint: `POST /admin/keys/rotate` (requires `X-Admin-Key`)

**Requirements:**

- Returns the new key(s) in the response
- After rotation, old keys should no longer work
- Update docs with how to use it from Swagger

**Design choice (explain tradeoffs):**

- **Easy mode**: rotate keys in-memory (works until container restarts)
- **Real mode**: write new key(s) to SSM Parameter Store and restart/reload the API

---

## Part 2: Optional Individual Extensions

Pick **any 2** of these:

### A) Monitoring (Qdrant → CloudWatch dashboard)

Send Qdrant metrics to CloudWatch and build a dashboard. Make it "vector DB-specific" (collection size, point count, search latency, index behavior) not just CPU/RAM.

Qdrant exposes Prometheus-style metrics - scrape them and publish to CloudWatch.

### B) Explore the Qdrant dashboard

Use SSH port forwarding to access the Qdrant dashboard safely:

```bash
ssh -i <your-key.pem> -L 6333:localhost:6333 ec2-user@<EC2_PUBLIC_IP>
```

Then open: `http://localhost:6333/dashboard`

**What to do:**

- Find the `mem0` collection and inspect stored points/payloads
- Compare `infer=false` vs `infer=true` memories
- Notice semantic vs keyword search behavior

### C) API / Swagger refactor

Add a new endpoint or refactor request/response shapes and update docs.

### D) Data-minded extension

Export `/admin/all-memories` to CSV and build a small analysis notebook (topics, per-user counts, growth over time).

### Bonus (does not count toward "pick 2")

Move secrets out of `terraform.tfvars` and into SSM created out-of-band (AWS CLI/console), then modify Terraform to read them.

---

## Part 3: Team CI/CD Extension (Required)

**Team size:** 3-4 students

Build a GitHub Actions CI/CD pipeline as a team.

### Setup

**Repository Owner:**

1. Fork/clone the repo
2. Add team members as collaborators (Settings → Collaborators)
3. Set up branch protection (Settings → Branches):
   - Branch pattern: `main`
   - Require PR before merging
   - Require status checks to pass
4. Create GitHub Project (Projects → New → "Team backlog" template)

**Team:**

Create Issues for each task:

- Setup GitHub Actions workflow structure
- Add Python linting (ruff or flake8)
- Add Terraform validation (fmt, validate)
- Add Docker build test
- Update documentation

Assign Issues to team members and drag to Kanban columns.

### Implementation

Create `.github/workflows/pr-validation.yml`:

```yaml
name: PR Validation

on:
  pull_request:
    branches: [main]

jobs:
  lint-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install ruff
      - name: Lint with ruff
        run: ruff check src/

  validate-terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - name: Terraform Format Check
        run: terraform fmt -check -recursive infra/terraform/
      - name: Terraform Validate
        run: |
          cd infra/terraform
          terraform init -backend=false
          terraform validate

  test-docker-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t mem0_api:test -f deployment/Dockerfile .
```

### Workflow

**Branch strategy:**

- Feature branches: `feature/lint-python`, `feature/terraform-validate`, etc.
- One Issue = one branch = one Pull Request

**PR process:**

1. Create feature branch
2. Make changes
3. Open PR to `main`
4. Request review from teammate
5. Wait for CI checks to pass
6. Get approval
7. Merge (squash and merge)
8. Move Issue to "Done"

### Deliverables

1. GitHub repo with:

   - `.github/workflows/*.yml` file(s)
   - Branch protection enabled
   - All team members have commits

2. GitHub Project board:

   - All Issues in "Done"
   - Clear task history

3. At least 3-5 Pull Requests:

   - Code review on each PR
   - CI checks passing

4. Write-up (`TEAM_WRITEUP.md`):
   - What you automated and why
   - Challenges faced
   - How you divided the work
   - What you'd automate next

### Stretch Goals

If you finish early:

- Add security scanning (`pip-audit`, `tfsec`/`Checkov`)
- Add test coverage (`pytest` in CI)
- Add deployment automation (Docker Hub/AWS ECR)
- Add status badges to README

### Common Issues

**Workflow doesn't trigger:**

- File must be in `.github/workflows/`
- Check `on:` trigger syntax
- Validate YAML syntax

**Terraform validate fails:**

- Run `terraform init -backend=false` first
- Test locally before pushing

**Docker build fails:**

- Test locally: `docker build -t test -f deployment/Dockerfile .`
- Check `COPY` statements in Dockerfile

### Resources

- [GitHub Actions Quickstart](https://docs.github.com/en/actions/quickstart)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [ruff](https://docs.astral.sh/ruff/) (Python linter)

---

**Ready to start?** Form your teams and begin with the CI/CD extension!
