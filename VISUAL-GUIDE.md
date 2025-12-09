# Visual Guide: Complete CI/CD Pipeline Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      YOUR LOCAL MACHINE                         │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Source Code                                            │   │
│  │ ├─ main.py          (FastAPI Application)             │   │
│  │ ├─ test.py          (Test Suite)                      │   │
│  │ ├─ requirements.txt  (Dependencies)                   │   │
│  │ ├─ Dockerfile       (Container Config)                │   │
│  │ └─ ...other files                                     │   │
│  └────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                      git push origin main                      │
│                           │                                    │
└───────────────────────────┼────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────────┐
         │      GITHUB REPOSITORY               │
         │  https://github.com/username/        │
         │       CICD-Practice                  │
         │                                      │
         │  .github/workflows/ci-cd.yml         │
         │  (Workflow Triggered!)               │
         └──────────────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │ Workflow Runs │
                    └───────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
    ┌────────┐         ┌────────┐         ┌──────────────┐
    │  TEST  │         │SECURITY│         │BUILD & PUSH  │
    │  JOB   │         │ SCAN   │         │ DOCKER JOB   │
    │        │         │ JOB    │         │              │
    │(Runs   │         │(Runs   │         │(Runs ONLY    │
    │ 3x:    │         │every   │         │ if tests &   │
    │ Py3.9  │         │ push)  │         │ scan pass!)  │
    │ Py3.10 │         │        │         │              │
    │ Py3.11)│         │        │         │              │
    └────┬───┘         └───┬────┘         └──────┬───────┘
         │                 │                     │
    ├─Install deps    ├─Bandit scan      ├─Docker build
    ├─Run pytest      ├─Upload report    ├─Push to ghcr.io
    ├─Flake8 check                       ├─Tag image
    ├─Black check
    └─Upload results
         │                 │                     │
         └─────────────────┼─────────────────────┘
                           │
              (All jobs complete in ~2-3 min)
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
        ▼                                     ▼
    ┌────────────────────┐          ┌──────────────────────┐
    │   GITHUB ACTIONS   │          │      DOCKER IMAGE    │
    │   Workflow Report  │          │  IN REGISTRY (ghcr) │
    │                    │          │                      │
    │ ✅ All Tests Passed│          │ ghcr.io/username/    │
    │ ✅ Security OK     │          │ cicd-practice:main   │
    │ ✅ Docker Built    │          │ cicd-practice:latest │
    │ ✅ Pushed to GHCR  │          │ cicd-practice:sha-.. │
    │                    │          │                      │
    │ Artifacts:         │          │ Ready to Deploy! 🚀  │
    │ • Test results     │          │                      │
    │ • Coverage report  │          │ Pull anytime:        │
    │ • Security report  │          │ docker pull ghcr.io/ │
    │                    │          │ ...                  │
    └────────────────────┘          └──────────────────────┘
```

## Job Dependency Graph

```
START (Code pushed to main)
    │
    ├─────────┬──────────────────────┐
    │         │                      │
    ▼         ▼                      ▼
  TEST    SECURITY-SCAN          (runs parallel)
    │         │
    │    (generates report)       
    │         │
    └────┬────┘
         │
    Both PASS?
         │
       ┌─┴─┐
       YES NO
       │   │
       ▼   ▼
    NEXT STOP
    │      (don't build docker)
    ▼
BUILD-AND-PUSH
    │
    ├─ Docker build
    ├─ Push to registry
    └─ Tag image
       │
       ▼
    SUCCESS ✅
    Docker image ready for deployment
```

## File Structure

```
CICD-Practice/
│
├── 📁 .github/
│   └── 📁 workflows/
│       └── 📄 ci-cd.yml              ← Workflow configuration
│                                        (The magic happens here!)
│
├── 📁 Application Files
│   ├── 📄 main.py                    ← FastAPI app
│   ├── 📄 test.py                    ← Unit tests
│   └── 📄 requirements.txt            ← Python dependencies
│
├── 📁 Docker Files
│   ├── 📄 Dockerfile                 ← Container config
│   └── 📄 .dockerignore              ← Docker ignore rules
│
├── 📁 Git Files
│   └── 📄 .gitignore                 ← Git ignore rules
│
└── 📁 Documentation
    ├── 📄 README.md                  ← Project overview
    ├── 📄 CI-CD-GUIDE.md            ← Detailed CI/CD concepts
    ├── 📄 DOCKER-GUIDE.md           ← Docker guide
    ├── 📄 QUICKSTART.md             ← Quick start
    ├── 📄 PIPELINE-SUMMARY.md       ← Pipeline overview
    ├── 📄 PUSH-AND-MONITOR.md       ← Setup instructions
    └── 📄 PRE-PUSH-CHECKLIST.md     ← Pre-push checks
```

## Workflow Execution Timeline

```
TIME    EVENT                               STATUS
────────────────────────────────────────────────────────────
0s      Workflow triggered                  📍 Starting
        (push to main detected)

5s      Set up test runners                 ⚙️  Setting up
        (Python 3.9, 3.10, 3.11)

10s     Install dependencies (parallel)     📦 Downloading
        (Pip cache helps)

15s     TEST: Run pytest                    🧪 Testing
        (3 versions simultaneously)

30s     TEST: Code quality checks           ✅ Validating
        (flake8, black)

35s     SECURITY: Bandit scan               🔒 Scanning
        (vulnerability check)

45s     All tests & scans passed?           ✓  Verified

50s     BUILD: Docker Buildx setup          🐳 Building
        (advanced builder)

55s     BUILD: Auth to registry             🔐 Authenticating
        (GitHub Container Registry)

60s     BUILD: Extract metadata             🏷️  Tagging
        (branch, SHA, version tags)

70s     BUILD: Build Docker image           🔨 Compiling
        (layers cached for speed)

120s    BUILD: Push to registry             📤 Uploading
        (image to ghcr.io)

150s    COMPLETE                            ✅ SUCCESS!
        Image available in registry
```

## What Each Job Does

### 1️⃣ TEST JOB (Runs 3x in parallel)

```
Python 3.9 Runner          Python 3.10 Runner       Python 3.11 Runner
│                          │                        │
├─ Checkout code           ├─ Checkout code        ├─ Checkout code
├─ Setup Python 3.9        ├─ Setup Python 3.10    ├─ Setup Python 3.11
├─ Cache pip               ├─ Cache pip            ├─ Cache pip
├─ Install deps            ├─ Install deps         ├─ Install deps
├─ Run pytest              ├─ Run pytest           ├─ Run pytest
├─ Flake8 check            ├─ Flake8 check         ├─ Flake8 check
├─ Black check             ├─ Black check          ├─ Black check
└─ Upload results          └─ Upload results       └─ Upload results
   (all 3 run simultaneously,     (takes ~45s total)
    each takes ~45s)
```

### 2️⃣ SECURITY-SCAN JOB

```
Checkout code
    │
    ▼
Install Bandit
    │
    ▼
Scan main.py for vulnerabilities
    │
    ├─ Check for SQL injection risks
    ├─ Check for hardcoded secrets
    ├─ Check for insecure functions
    └─ Generate JSON report
    │
    ▼
Upload security report
    (Available in artifacts)
```

### 3️⃣ BUILD-AND-PUSH JOB (Only if 1 & 2 pass)

```
Setup Docker Buildx
    │
    ▼
Authenticate to GHCR
    │
    ├─ Registry: ghcr.io
    ├─ Username: ${{ github.actor }}
    └─ Token: ${{ secrets.GITHUB_TOKEN }}
    │
    ▼
Extract metadata
    │
    ├─ Branch: main
    ├─ SHA: abc123def...
    ├─ Tags to apply:
    │  • main (branch name)
    │  • latest (only on main)
    │  • sha-abc123def (commit)
    └─ Create labels
    │
    ▼
Build Docker image
    │
    ├─ FROM python:3.11-slim
    ├─ WORKDIR /app
    ├─ RUN pip install -r requirements.txt
    ├─ COPY main.py .
    └─ CMD ["uvicorn", "main:app", ...]
    │
    ├─ Use GHA cache for layers
    └─ (super fast on subsequent runs!)
    │
    ▼
Push to registry
    │
    ├─ Upload layers
    ├─ Apply tags
    └─ Make available worldwide
    │
    ▼
Image ready at:
    ghcr.io/YOUR_USERNAME/cicd-practice:latest
```

## Data Flow

```
GitHub Repository
│
├─ Stores code
├─ Stores workflow config (.github/workflows/ci-cd.yml)
├─ Stores artifacts (test results, reports)
├─ Has package registry (ghcr.io)
└─ Provides GITHUB_TOKEN (automatic auth)
    │
    ▼
GitHub Actions Runners (Temporary VMs)
    │
    ├─ Checkout repository code
    ├─ Run test jobs (3 Python versions)
    ├─ Run security scan
    ├─ Build Docker image
    └─ Push to registry
    │
    ▼
GitHub Container Registry (ghcr.io)
    │
    ├─ Stores your Docker images
    ├─ One URL for all versions
    ├─ Accessible worldwide
    └─ You can pull anytime
        │
        ▼
    Your Deployment Platform
        │
        ├─ AWS
        ├─ Heroku
        ├─ DigitalOcean
        ├─ Kubernetes
        └─ Any Docker-compatible platform
```

## Security & Permissions

```
GITHUB_TOKEN (Automatic)
    │
    ├─ Provided by GitHub Actions
    ├─ No manual secrets needed
    ├─ Scoped to repository
    └─ Permissions set in workflow:
        │
        ├─ contents: read (read code)
        ├─ packages: write (push images)
        └─ Automatically revoked after workflow
```

## Caching Strategy

```
First Build              Subsequent Builds
│                        │
├─ Download all deps     ├─ Restore from cache
├─ Build all layers      ├─ Reuse unchanged layers
├─ Slower: ~2-3 min      ├─ Super fast: ~1-1.5 min
│                        │
└─ Save to cache         └─ Update cache only if changed
                            (smart caching!)
```

## Deployment Pipeline (Next Step)

```
After Docker image is pushed to ghcr.io:

ghcr.io/username/cicd-practice:latest
    │
    ├─ Deploy to AWS ECS
    ├─ Deploy to Heroku
    ├─ Deploy to DigitalOcean App Platform
    ├─ Deploy to Google Cloud Run
    ├─ Deploy to Kubernetes
    └─ Deploy to any Docker registry
```

## Success Indicators

```
GREEN ✅ = All systems go!

┌─────────────────────────────────┐
│ GitHub Actions Dashboard        │
├─────────────────────────────────┤
│ ✅ test [Completed]             │
│    ├─ 3.9 ✅                    │
│    ├─ 3.10 ✅                   │
│    └─ 3.11 ✅                   │
│ ✅ security-scan [Completed]    │
│ ✅ build-and-push [Completed]   │
│                                 │
│ All checks passed! 🎉           │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ GitHub Packages Registry        │
├─────────────────────────────────┤
│ 📦 cicd-practice                │
│    ├─ main (latest)             │
│    ├─ sha-abc123def             │
│    └─ (ready to deploy!)        │
└─────────────────────────────────┘
```

This is your complete CI/CD pipeline! 🚀
