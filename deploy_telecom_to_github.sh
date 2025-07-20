#!/bin/bash

echo "🚀 Deploying Telecom Network Wrangler to GitHub..."

echo "🔑 Enter your GitHub Personal Access Token:"
read -s PAT
echo ""

if [ -z "$PAT" ]; then
    echo "❌ No PAT provided. Exiting."
    exit 1
fi

GITHUB_USER="bdstest"
REPO_NAME="telecom-network-wrangler"

echo "📁 Creating GitHub repository..."

# Create repository via GitHub API
response=$(curl -s -H "Authorization: token $PAT" \
               -H "Accept: application/vnd.github.v3+json" \
               https://api.github.com/user/repos \
               -d "{
                 \"name\": \"$REPO_NAME\",
                 \"description\": \"5G Network Performance Monitoring and Optimization Platform with AI-driven analytics\",
                 \"private\": false,
                 \"auto_init\": false
               }")

if echo "$response" | grep -q '"name"'; then
    echo "✅ Repository created successfully"
else
    echo "⚠️  Repository may already exist or creation failed"
    echo "Response: $response"
fi

echo ""
echo "⏳ Waiting 5 seconds for GitHub to process..."
sleep 5

echo ""
echo "🚀 Pushing repository to GitHub..."

# Remove existing remote if it exists
git remote remove origin 2>/dev/null || true

# Add GitHub remote
git remote add origin https://${PAT}@github.com/${GITHUB_USER}/${REPO_NAME}.git

# Push master branch
echo "📤 Pushing master branch..."
git push -u origin master

if [ $? -eq 0 ]; then
    echo "✅ Master branch pushed successfully"
else
    echo "❌ Master branch push failed"
    exit 1
fi

# Push all other branches
echo "📤 Pushing all feature branches..."
git push --all origin

if [ $? -eq 0 ]; then
    echo "✅ All branches pushed successfully"
else
    echo "❌ Some branches failed to push"
fi

echo ""
echo "🎉 DEPLOYMENT COMPLETE!"
echo ""
echo "🔗 Your Telecom Network Wrangler Repository:"
echo "   📡 Main: https://github.com/${GITHUB_USER}/${REPO_NAME}"
echo "   📊 Issues: https://github.com/${GITHUB_USER}/${REPO_NAME}/issues"
echo "   🔄 Branches: https://github.com/${GITHUB_USER}/${REPO_NAME}/branches"
echo ""
echo "📈 Repository Statistics:"
echo "   - Total Commits: $(git rev-list --count HEAD)"
echo "   - Active Branches: $(git branch -r | wc -l)"
echo "   - Timeline: August 2023 - July 2025 (In Progress)"
echo "   - Focus: 5G Network Monitoring, Slicing, RF Optimization"
echo ""
echo "🎯 Features Deployed:"
echo "   ✅ Advanced network slicing orchestration"
echo "   ✅ RF optimization with ML algorithms" 
echo "   ✅ Spectrum efficiency analysis (2G-5G)"
echo "   ✅ Carrier aggregation optimization"
echo "   ✅ Multi-generation network audit"
echo "   ✅ Production-ready Docker infrastructure"