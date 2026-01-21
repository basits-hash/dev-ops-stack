#!/bin/bash

# GitHub Pages Deployment Helper Script

set -e

echo "🚀 GitHub Pages Deployment Helper"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if git is initialized
if [ ! -d .git ]; then
    print_warning "Git not initialized. Initializing..."
    git init
    print_status "Git initialized"
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo ""
    print_info "No remote found. Please enter your GitHub repository URL:"
    read -p "Repository URL (e.g., https://github.com/username/repo.git): " repo_url
    git remote add origin "$repo_url"
    print_status "Remote added"
fi

# Get current branch
current_branch=$(git rev-parse --abbrev-ref HEAD)

# Check if on main branch
if [ "$current_branch" != "main" ]; then
    print_warning "Not on main branch. Switching to main..."
    git checkout -b main 2>/dev/null || git checkout main
fi

echo ""
print_info "Preparing to deploy..."

# Add all files
git add .
print_status "Files staged"

# Commit
read -p "Enter commit message (or press enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy to GitHub Pages with demo mode"
fi

git commit -m "$commit_msg" || echo "No changes to commit"
print_status "Changes committed"

echo ""
print_info "Pushing to GitHub..."
git push -u origin main

echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ Code pushed to GitHub!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Go to your repository on GitHub"
echo "2. Click 'Settings' → 'Pages'"
echo "3. Under 'Source', select 'GitHub Actions'"
echo "4. Wait 2-3 minutes for deployment"
echo ""
echo "Your site will be live at:"
echo "👉 https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
print_status "Deployment initiated!"
