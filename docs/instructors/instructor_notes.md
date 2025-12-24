# Quick Instructor Notes

Start: [`README.md`](README.md) • Student guide: [`../students/README.md`](../students/README.md)

## Pre-Class Setup (5 min)
1. Provision EC2 instances (one per student)
2. Distribute SSH keys
3. Test one deployment yourself
4. Ensure AWS Bedrock is enabled in your region and model access is granted

## Class Flow (90 min)

### Introduction (10 min)
- Explain what we're building
- Show final result
- Discuss use cases

### Hands-On Deployment (55 min)
- Students follow [`../students/setup.md`](../students/setup.md)
- Walk through steps together
- Help with troubleshooting

### Testing & Exploration (15 min)
- Run [`../../scripts/test_api.sh`](../../scripts/test_api.sh)
- Explore Swagger UI
- Try custom queries

### Wrap-Up (10 min)
- Q&A
- Discuss extensions
- Share resources

## Common Questions

Q: "Can I use this in production?"
A: Yes, but add: SSL, rate limiting, monitoring, backups

Q: "How much will this cost?"
A: Mostly EC2 cost (~$30/month for a single always-on instance). Bedrock usage varies by model/traffic and is typically pennies for lab testing.

Q: "Can I modify the code?"
A: Absolutely! It's yours. Check src/ directory.

Q: "What if OpenAI is down?"
A: If using the OpenAI provider track, the API will run but embedding/LLM features won’t work. In the default AWS track, this is not relevant.

Q: "Can we stay fully inside AWS (no OpenAI)?"
A: Yes. This is the default track for this lab. See [`../students/setup.md`](../students/setup.md) (Terraform recommended).

## Success Metrics
- All students deploy successfully
- Everyone can add & search memories
- Students understand the architecture
- Can explain vector vs relational DBs

## Cleanup After Class
sudo docker stop mem0_api mem0_qdrant
sudo docker rm mem0_api mem0_qdrant
# OR terminate EC2 instances

## Cost
Per student: ~$0.10 for 2-hour lab
Class of 30: ~$3.00 total

## Files Students Need
- README.md (overview)
- docs/students/setup.md (deployment steps)
- docs/students/api.md (endpoint reference)
- scripts/test_api.sh (testing)
- All code files (src/, deployment/, requirements.txt, .env.template)

## Files YOU Need
- docs/instructors/lab_guide.md (teaching guide)
- docs/instructors/instructor_notes.md (this file)

Good luck!

