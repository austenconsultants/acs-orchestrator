#!/bin/bash
# Setup all ACS repositories on GitHub

echo "=== ACS GitHub Setup Script ==="
echo ""
read -p "Enter your GitHub organization/username: " GITHUB_ORG
read -p "Enter your GitHub personal access token: " GITHUB_TOKEN

# Configure git
git config --global user.name "ACS System"
git config --global user.email "acs@system.local"

# List of all repositories
REPOS=(
    "acs-orchestrator"
    "acs-chat-hub"
    "agent-acs-voice-hub"
    "agent-acs-voice-agent"
    "agent-acs-context"
    "agent-acs-agent"
    "agent-acs-voice"
    "agent-acs-voice-assistant"
)

echo ""
echo "Creating/updating repositories on GitHub..."

for repo in "${REPOS[@]}"; do
    echo ""
    echo "Processing: $repo"
    
    # Check if local repo exists
    if [ -d "/opt/github-agents/$repo" ]; then
        cd "/opt/github-agents/$repo"
        
        # Create GitHub repo if it doesn't exist
        curl -s -H "Authorization: token $GITHUB_TOKEN" \
             -d "{\"name\":\"$repo\", \"description\":\"ACS Component: $repo\", \"private\":false}" \
             https://api.github.com/user/repos > /dev/null
        
        # Add remote if not exists
        if ! git remote | grep -q origin; then
            git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_ORG/$repo.git"
        else
            git remote set-url origin "https://$GITHUB_TOKEN@github.com/$GITHUB_ORG/$repo.git"
        fi
        
        # Push to GitHub
        git branch -M main 2>/dev/null
        git push -u origin main --force
        
        echo "✅ $repo pushed to GitHub"
    else
        echo "⚠️  $repo not found locally"
    fi
done

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Your repositories are now on GitHub:"
for repo in "${REPOS[@]}"; do
    echo "  https://github.com/$GITHUB_ORG/$repo"
done
echo ""
echo "Next steps:"
echo "1. Update the UI in v0 with agent tabs"
echo "2. Deploy the Context Service"
echo "3. Create PostgreSQL tables"
echo "4. Test the complete system"
