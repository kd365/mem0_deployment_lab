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
- Make it "vector DB-specific" (not just CPU/RAM): things like collection size / point count growth, search request latency, and index behavior.
- Implementation hint: Qdrant exposes Prometheus-style metrics; scrape them and publish to CloudWatch (multiple valid AWS approaches).

### 2) Explore the Qdrant dashboard (port 6333)

Goal: learn what Qdrant stores and what "a vector database" looks like in practice.

- **Recommended (safe)**: use SSH port forwarding, then open the dashboard locally:
  - `ssh -i <your-key.pem> -L 6333:localhost:6333 ec2-user@<EC2_PUBLIC_IP>`
  - Open: `http://localhost:6333/dashboard`
- **Alternate (less safe)**: set `expose_qdrant_public = true` in Terraform (this opens port 6333 to the internet).

What to do in the dashboard:

- Find the `mem0` collection and inspect stored points/payloads (what fields exist? where is `user_id`?).
- Compare "raw memories" (`infer=false`) vs "extracted facts" (`infer=true`) by looking at the text stored.
- Notice how "search" is vector-based (semantic) vs keyword-based (exact match).

How to improve it (design ideas):

- Make access safer (do not expose 6333 publicly; keep SSH tunneling or add auth/reverse proxy).
- Add dashboard notes/screenshots to the lab docs (what students should look for).
- (Stretch) Pin the Qdrant image tag for repeatable classroom behavior.

### 3) API / Swagger refactor

- Add a new endpoint or refactor request/response shapes and update docs.

### 4) Data-minded extension

- Export `/admin/all-memories` results to CSV and build a small analysis notebook (topics, per-user counts, growth over time).

### Bonus (does not count toward the "pick any 2")

- **SSM-first secrets**: move any secrets out of `terraform.tfvars` and into SSM created out-of-band, then modify Terraform to read them.

---

## Team Assignment: CI/CD Extension (1 Day)

This is a **1-day team extension** (3-4 students per team) where you take what you built in the lab and add GitHub Actions CI/CD automation.

**What you'll build:**

- GitHub Actions workflow for automated testing and validation
- Team project board using GitHub Projects (Kanban)
- Collaborative workflow using Issues and Pull Requests

**Duration:** 1 day (in-class or homework)

---

## Part 1: Team Setup (30 minutes)

### Step 1: Form Your Team (3-4 students)

Choose one person to be the **Repository Owner** (they'll set up the repo and project board).

### Step 2: Repository Setup (Repository Owner)

1. **Fork or clone** the `mem0_deployment_lab` repo to your personal GitHub account

2. **Add team members as collaborators:**

   - Go to: Settings → Collaborators → Add people
   - Add each team member (they need write access)

3. **Set up branch protection:**
   - Go to: Settings → Branches → Add branch protection rule
   - Branch name pattern: `main`
   - Check: "Require a pull request before merging"
   - Check: "Require status checks to pass before merging" (after you create the workflow)

### Step 3: GitHub Project Board Setup (Repository Owner)

1. **Create a new GitHub Project:**

   - Go to your repo → Projects tab → "Link a project" → "New project"
   - Choose template: **"Team backlog"** (Kanban style)
   - Name it: `Mem0 CI/CD Sprint`

2. **Create initial Issues** (divide these among the team):

   - `Setup GitHub Actions workflow structure`
   - `Add Python linting (ruff or flake8)`
   - `Add Terraform validation (fmt, validate)`
   - `Add Docker build test`
   - `Add deployment workflow (optional)`
   - `Update documentation`

3. **Assign Issues:**
   - Each team member takes 1-2 Issues
   - Drag Issues to appropriate columns (Backlog → Ready → In Progress → Done)

---

## Part 2: CI/CD Implementation (3-4 hours)

### What to Automate

Look at your existing Mem0 deployment and decide what makes sense to automate. Here are suggested starting points:

#### Option 1: Testing & Validation (Recommended for 1-day)

Create `.github/workflows/pr-validation.yml`:

**What it should do:**

- Run on every Pull Request
- Lint Python code (use `ruff`, `flake8`, or `black`)
- Validate Terraform (`terraform fmt -check`, `terraform validate`)
- Build Docker image (don't push, just verify it builds)

**Example structure:**

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

#### Option 2: Deployment Automation (Stretch Goal)

If your team finishes Option 1 quickly, add a deployment workflow that builds and pushes Docker images to Docker Hub or AWS ECR on merge to `main`.

**Note:** This requires setting up GitHub Secrets for credentials.

### Team Workflow

1. **Branch strategy:**

   - Create feature branches: `feature/lint-python`, `feature/terraform-validate`, etc.
   - One Issue = one branch = one Pull Request

2. **Pull Request process:**

   - Open a PR from your feature branch to `main`
   - Request review from at least one teammate
   - Wait for CI checks to pass (GitHub Actions)
   - Get approval
   - Merge (use "Squash and merge")
   - Move Issue to "Done" on Project board

3. **Code reviews:**
   - Review each other's PRs (don't merge your own!)
   - Check: does the workflow YAML syntax look correct?
   - Check: are the commands reasonable?
   - Approve or request changes

---

## Part 3: Testing & Verification (1 hour)

### Demonstrate Your CI/CD Pipeline

1. **Make a test change:**

   - Pick a file to modify (e.g., add a comment to `src/app.py`)
   - Create a branch
   - Open a PR

2. **Show CI in action:**

   - Point to the "Checks" tab on your PR
   - Show the workflow running
   - Show it passing (or failing, then fix it!)

3. **Show your Project board:**
   - All Issues should be in "Done"
   - Show the history of your work (who did what)

### Deliverables (What to Submit)

1. **GitHub repository** with:

   - At least one `.github/workflows/*.yml` file
   - Branch protection rules enabled
   - All team members have commits in the history

2. **GitHub Project board** with:

   - All Issues moved to "Done"
   - Clear history of task progression

3. **At least 3-5 Pull Requests** (one per team member minimum):

   - Each PR should have a code review from another team member
   - CI checks should pass on each PR

4. **Brief write-up** (add to `README.md` or create `TEAM_WRITEUP.md`):
   - What did you automate and why?
   - What challenges did you face?
   - How did you divide the work?
   - What would you automate next if you had more time?

---

## Grading Rubric (Total: 50 points)

### GitHub Actions Workflow (25 points)

- [ ] Workflow file exists and is syntactically correct (5 pts)
- [ ] Runs on Pull Requests automatically (5 pts)
- [ ] Includes at least 2 meaningful checks (lint, validate, build) (10 pts)
- [ ] Workflow actually runs and passes (5 pts)

### Team Collaboration (15 points)

- [ ] GitHub Project board set up with Kanban columns (3 pts)
- [ ] Issues created and assigned (3 pts)
- [ ] All team members have commits (3 pts)
- [ ] Pull Requests used (not direct commits to main) (3 pts)
- [ ] Code reviews conducted (comments/approvals visible) (3 pts)

### Documentation (10 points)

- [ ] Write-up explains what was automated and why (5 pts)
- [ ] Write-up includes challenges and learnings (3 pts)
- [ ] README or docs updated to reflect CI/CD setup (2 pts)

---

## Tips & Hints

### GitHub Actions Syntax

- Use the **Actions** tab in your repo to see workflow runs
- Click on a workflow run to see logs
- YAML indentation matters! Use 2 spaces (not tabs)

### Common Issues

**Problem:** Workflow doesn't trigger

- Check: is your YAML file in `.github/workflows/`?
- Check: is the `on:` trigger correct? (`pull_request`, `push`, etc.)
- Check: YAML syntax valid? (use a linter)

**Problem:** Terraform validate fails

- Make sure you run `terraform init -backend=false` first (CI doesn't have your S3 backend)
- Check: are your Terraform files valid locally?

**Problem:** Docker build fails in CI

- Check: does it build locally? (`docker build -t test -f deployment/Dockerfile .`)
- Check: are all files copied into the image (`COPY` statements in Dockerfile)?

### Collaboration Tips

- **Communicate!** Use GitHub Issues comments, Slack, or Discord
- **Divide & conquer:** Each person takes one workflow job
- **Test locally first:** Don't push untested YAML to GitHub (saves CI minutes)
- **Review thoroughly:** Catch issues in PRs before merging

---

## Stretch Goals (Optional)

If your team finishes early:

1. **Add security scanning:**

   - Use `pip-audit` to scan Python dependencies for vulnerabilities
   - Use `tfsec` or `Checkov` to scan Terraform for security issues

2. **Add test coverage:**

   - Write a simple unit test for one function in `src/`
   - Run with `pytest` in CI

3. **Add deployment automation:**

   - Build and push Docker image to Docker Hub or AWS ECR
   - Trigger on merge to `main` (not on PRs)

4. **Add status badges:**
   - Add a GitHub Actions status badge to your `README.md` (shows build passing/failing)

---

## Resources

**GitHub Actions:**

- [GitHub Actions Quickstart](https://docs.github.com/en/actions/quickstart)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions) (pre-built actions)

**GitHub Projects:**

- [About Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [Quickstart for Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects)

**Tools:**

- [ruff](https://docs.astral.sh/ruff/) (Python linter)
- [Terraform CLI](https://developer.hashicorp.com/terraform/cli/commands)
- [Docker build](https://docs.docker.com/engine/reference/commandline/build/)

---

## FAQ

**Q: Do we need to deploy to AWS in this assignment?**

A: No. Focus on CI checks (linting, validation, build tests). Deployment is a stretch goal.

**Q: Can we use a different CI tool (e.g., GitLab CI, Jenkins)?**

A: No, GitHub Actions is required since you're using GitHub for the repo and project board.

**Q: What if we don't have time to automate everything?**

A: Start with Python linting and Terraform validation. That's enough to demonstrate CI/CD concepts.

**Q: Do we need AWS credentials in GitHub Secrets?**

A: Only if you attempt the deployment stretch goal. For basic validation, you don't need AWS access.

**Q: What if a team member isn't contributing?**

A: Document this in your write-up. Instructor can see individual contributions via Git commits and PR activity.

---

**Ready to start?** Begin with Part 1: Team Setup!
