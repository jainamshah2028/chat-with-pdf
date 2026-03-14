# 🚀 GitHub Setup & Deployment Guide

This guide walks you through setting up your Chat with PDF repository on GitHub and preparing for deployment.

## Prerequisites

1. **GitHub Account** — Create one at https://github.com
2. **Git Installed** — Download from https://git-scm.com
3. **GitHub Authentication** — SSH keys or Personal Access Token

---

## Step 1: Initialize Git Repository (Local)

```bash
# Navigate to project directory
cd chat_with_pdf

# Initialize git (only first time)
git init

# Configure git (one-time setup)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Or set globally for all projects
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Step 2: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `chat_with_pdf` (must match folder name)
   - **Description**: "AI-powered PDF chat application"
   - **Visibility**: `Public` (for open-source) or `Private`
   - **Initialize repository**: ❌ Leave unchecked (we already have files)
3. Click **Create repository**

You'll see instructions. Copy the repository URL (HTTPS or SSH).

---

## Step 3: Connect Local to Remote Repository

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/chat_with_pdf.git
# OR use SSH (requires SSH keys configured):
# git remote add origin git@github.com:YOUR_USERNAME/chat_with_pdf.git

# Verify remote is added
git remote -v
# Output should show:
# origin  https://github.com/YOUR_USERNAME/chat_with_pdf.git (fetch)
# origin  https://github.com/YOUR_USERNAME/chat_with_pdf.git (push)
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

## Step 4: Prepare Files for First Commit

### Stage All Files

```bash
# Add all files
git add .

# Review what's staging to commit
git status

# Should show:
# - Added: .gitignore, LICENSE, Dockerfile, docs/*, etc.
# - All important files ready
# - .env, __pycache__, venv/ should NOT appear
```

### Verify .gitignore is Working

```bash
# Check .env is ignored
git status | grep ".env"
# Should return nothing (means it's properly ignored)

# List all ignored files
git check-ignore -v **/*
```

---

## Step 5: Make First Commit

```bash
# Write a meaningful commit message
git commit -m "Initial commit: GitHub-optimized project setup

- Consolidate to app_enhanced.py as primary version
- Add comprehensive documentation (SETUP, DEPLOYMENT, API_PROVIDERS, ARCHITECTURE)
- Add CI/CD workflows (GitHub Actions for testing, linting, coverage)
- Add Docker support (Dockerfile, docker-compose.yml)
- Add development tooling (pytest, black, flake8, pre-commit)
- Create MIT license for open-source
- Create contributing guidelines
- Add extensive environment configuration"
```

---

## Step 6: Push to GitHub

```bash
# Push to remote repository
git push -u origin main
# If main branch doesn't exist, Git will create it

# Alternative: push to master branch
# git push -u origin master

# Verify push was successful
git log --oneline
# Should show your commit in the log
```

If prompted for authentication:
- **HTTPS**: Use Personal Access Token instead of password
- **SSH**: Ensure SSH keys are configured

---

## Step 7: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/chat_with_pdf`
2. Check that:
   - ✅ All files are present
   - ✅ README.md displays properly
   - ✅ `.gitignore` is preventing secrets exposure
   - ✅ LICENSE is visible

---

## Authentication Setup

### Option A: HTTPS with Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token (classic)"** or **"Generate new token"**
3. Select scopes: `repo` (full control of repositories)
4. Copy the token
5. When Git asks for password, paste the token instead

```bash
# Use credential helper to save token
git config --global credential.helper store
# Then push normally - token will be saved
git push -u origin main
```

### Option B: SSH Keys

```bash
# Generate SSH key (Windows/macOS/Linux)
ssh-keygen -t ed25519 -C "your.email@example.com"
# Press Enter to save in default location, then press Enter for no passphrase

# Display public key
cat ~/.ssh/id_ed25519.pub  # macOS/Linux
type %userprofile%\.ssh\id_ed25519.pub  # Windows PowerShell

# Copy the output, then:
# 1. Go to https://github.com/settings/keys
# 2. Click "New SSH key"
# 3. Paste the key
# 4. Click "Add SSH key"

# Test connection
ssh -T git@github.com
# Should output: Hi YOUR_USERNAME! You've successfully authenticated...
```

### Option C: GitHub CLI

```bash
# Install GitHub CLI from https://cli.github.com

# Login to GitHub
gh auth login

# Follow prompts to authenticate

# Now push normally
git push -u origin main
```

---

## Ongoing Development Workflow

### Before Each Commit

```bash
# 1. Format code
black .

# 2. Sort imports
isort .

# 3. Check linting
flake8 .

# 4. Run tests
pytest tests/ -v

# All at once:
black . && isort . && flake8 . && pytest tests/ -v
```

Or let pre-commit hooks do it:

```bash
# Install hooks (one-time)
pre-commit install

# Just commit normally
git add .
git commit -m "Your message"
# Hooks run automatically and fix code
```

### Making Changes

```bash
# Create feature branch
git checkout -b feat/my-feature-name

# Make changes...
git add .
git commit -m "feat: add feature description"

# Push to GitHub
git push origin feat/my-feature-name

# Open Pull Request on GitHub
# 1. Go to https://github.com/YOUR_USERNAME/chat_with_pdf
# 2. Click "Compare & pull request"
# 3. Write PR description
# 4. Click "Create pull request"
```

### Sync with Remote

```bash
# Update local with remote changes
git pull origin main

# See changes
git log --oneline -5
```

---

## Deploy to Streamlit Cloud

### 1. Connect Repository to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **"Deploy an app"**
4. Select:
   - **Repository**: YOUR_USERNAME/chat_with_pdf
   - **Branch**: main
   - **Main file path**: app_enhanced.py

### 2. Configure Secrets

1. Click **Settings** in app menu
2. Go to **Secrets** section
3. Paste your environment variables:

```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
DEFAULT_PROVIDER = "openai"
OPENAI_MODEL = "gpt-3.5-turbo"
```

### 3. Deploy

Click **Deploy** — Streamlit Cloud will build and host automatically!

Your app will be live at: `https://YOUR_USERNAME-chat-pdf.streamlit.app`

---

## Deploy with Docker

### 1. Push to GitHub Package Registry

```bash
# Login to GitHub
echo YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Build image
docker build -t ghcr.io/YOUR_USERNAME/chat-pdf:latest .

# Push to registry
docker push ghcr.io/YOUR_USERNAME/chat-pdf:latest
```

### 2. Deploy to Cloud

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for AWS, GCP, DigitalOcean, etc.

---

## Troubleshooting

### "fatal: remote origin already exists"

```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/YOUR_USERNAME/chat_with_pdf.git
```

### "Permission denied (publickey)"

```bash
# SSH key issue — use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/chat_with_pdf.git

# Or generate/add SSH key correctly
# See "Option B: SSH Keys" above
```

### "403 Forbidden"

```bash
# Token expired or insufficient permissions
# 1. Go to https://github.com/settings/tokens
# 2. Delete old token
# 3. Generate new token
# 4. Try pushing again
```

### Commits not appearing on GitHub

```bash
# Check remote configuration
git remote -v

# Check branch
git branch

# Check logs
git log --oneline

# Verify upstream tracking
git branch -vv
```

---

## Best Practices

✅ **Do:**
- Write clear, descriptive commit messages
- Use feature branches for new work
- Keep commits focused on single changes
- Test before pushing
- Review own changes before committing

❌ **Don't:**
- Commit API keys, passwords, secrets
- Commit large binary files (use Git LFS)
- Force push to main branch (`git push -f`)
- Leave uncommitted changes
- Ignore linting errors

---

## Branch Strategy

Follow **GitHub Flow** for simplicity:

```
main (production-ready)
  ↑
  └─ feature-branch-1 (work in progress)
     └─→ Pull Request → Merge to main

  └─ feature-branch-2
     └─→ Pull Request → Merge to main
```

### Branch Naming Convention

```bash
# Feature
git checkout -b feat/add-user-authentication

# Bug fix
git checkout -b fix/pdf-parsing-error

# Documentation
git checkout -b docs/update-readme

# Refactor
git checkout -b refactor/optimize-embeddings
```

---

## GitHub Actions Status

After pushing, check that CI/CD passes:

1. Go to your repo
2. Click **Actions** tab
3. See **Test** and **Code Quality** workflow runs
4. All checks should pass (green checkmarks)

---

## Useful GitHub Commands

```bash
# Clone a repository
git clone https://github.com/YOUR_USERNAME/chat_with_pdf.git

# See commit history
git log --oneline --graph --all

# See differences
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Stash changes temporarily
git stash

# List all branches
git branch -a

# Delete local branch
git branch -d branch-name
```

---

## Next Steps

1. ✅ Push to GitHub (this guide)
2. ✅ Deploy to Streamlit Cloud ([docs/DEPLOYMENT.md](docs/DEPLOYMENT.md))
3. ✅ Add collaborators (Settings → Collaborators)
4. ✅ Enable branch protection (Settings → Branches)
5. ✅ Set up issue templates (GitHub feature)
6. ✅ Promote on social media, GitHub topics, etc.

---

## Documentation Links

- 📚 [SETUP.md](SETUP.md) — Installation guide
- 🚀 [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) — Deployment options
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) — Contributing guidelines
- 🏗️ [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Project structure
- 🧪 [TESTING_GUIDE.md](TESTING_GUIDE.md) — Testing instructions

---

Questions? Open an [Issue](https://github.com/YOUR_USERNAME/chat_with_pdf/issues) on GitHub!
