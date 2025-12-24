# Mem0 Deployment Lab

**Self-hosted memory layer with FastAPI + Qdrant vector database**

> **Lab Objective:** Deploy a production-ready AI memory API on AWS (Bedrock + Titan + Qdrant) in ~30 minutes

---

## What You'll Build

```
Your App → FastAPI (Port 8000) → Mem0 SDK → Qdrant (Vector DB)
```

**Features:**

- REST API for AI memory management
- Semantic search with vector embeddings
- User isolation & session management
- AWS Bedrock (Titan embeddings + Bedrock LLM) for embeddings/LLM
- OpenAI support (optional provider track)
- Docker containerized deployment

---

## Prerequisites

- AWS account with Bedrock enabled in your region (and model access granted)
- Terraform installed (recommended)
- AWS credentials configured locally (AWS CLI, SSO, or assumed role)
- (Optional) OpenAI API key if you choose the OpenAI provider track

---

## Quick Start

### 1. Start Here (Students)

```bash
# Follow the step-by-step deploy + test guide
cat SETUP.md
```

### 2. Test Your API (Students)

```bash
./test_api.sh
```

### 3. Use Swagger UI (Students)

Visit: `http://YOUR_EC2_IP:8000/docs`

---

## What's Included

```
mem0_deployment_lab/
├── SETUP.md              # Students: deploy (Terraform recommended) + test
├── API.md                # Students: Swagger + endpoint examples
├── ARCHITECTURE.md       # Optional reading: how the stack works
├── LAB_GUIDE.md          # Instructors: lesson plan + timing + checkpoints
├── INSTRUCTOR_NOTES.txt  # Instructors: quick run-of-show + reminders
├── src/                  # FastAPI application
├── deployment/           # Docker configuration
├── requirements.txt      # Python dependencies
├── .env.template         # Environment variables template
└── test_api.sh           # API test script
```

---

## Stack Components

| Component  | Technology                      | Port |
| ---------- | ------------------------------- | ---- |
| API Server | FastAPI + Mem0 SDK              | 8000 |
| Vector DB  | Qdrant                          | 6333 |
| Embeddings | AWS Bedrock (Titan)             | -    |
| LLM        | AWS Bedrock (e.g., Claude)      | -    |

---

## Cost Estimate (Rough)

- EC2 t3.medium: ~$30/month
- Bedrock usage: varies by model and traffic (typically pennies for lab usage)
- **Total: ~$30/month + model usage**

---

## Documentation

- **Students (do in order)**
  - `SETUP.md`: deploy + verify (Terraform recommended)
  - `API.md`: Swagger + copy/paste examples for each endpoint
  - `test_api.sh`: smoke tests against the API
  - `ARCHITECTURE.md` (optional): understand embeddings, vector DBs, and Mem0’s infer pipeline
- **Instructors**
  - `LAB_GUIDE.md`: structure, timing, checkpoints, extensions
  - `INSTRUCTOR_NOTES.txt`: quick reminders and common student pitfalls
- **Infrastructure**
  - `infra/terraform/README.md`: Terraform details (inputs/outputs, what gets created)
- **Interactive docs**
  - Swagger UI: `http://your-server:8000/docs`

---

## Support

- Mem0 Docs: https://docs.mem0.ai
- Qdrant Docs: https://qdrant.tech/documentation/

---

**Ready to deploy?** Open `SETUP.md`
