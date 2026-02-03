#!/bin/bash
# Example Git usage with DataHosting Gitea

read -p "Gitea Username: " GITEA_USER
read -p "API Secret (password): " API_SECRET
read -p "Repository name: " REPO_NAME

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "GIT COMMANDS:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "# Clone existing repository:"
echo "git clone https://$GITEA_USER:$API_SECRET@git.datahosting.company/$GITEA_USER/$REPO_NAME.git"
echo ""

echo "# Create new repository:"
echo "cd ~/my-project"
echo "git init"
echo "git add ."
echo "git commit -m 'Initial commit'"
echo "git remote add origin https://$GITEA_USER:$API_SECRET@git.datahosting.company/$GITEA_USER/$REPO_NAME.git"
echo "git push -u origin master"
echo ""

echo "# Or store credentials once:"
echo "git config --global credential.helper store"
echo "git clone https://git.datahosting.company/$GITEA_USER/$REPO_NAME.git"
echo "(Enter username and password when prompted)"
