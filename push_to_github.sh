#!/bin/bash
# Commands to run AFTER creating the GitHub repository

echo "🚀 Pushing Enhanced PDF Chat App to GitHub"
echo "Make sure you've created the repository on GitHub first!"
echo ""

# Push to GitHub
echo "📤 Pushing commits..."
git push -u origin master

# Verify success
echo "✅ Checking remote status..."
git remote -v

echo ""
echo "🎉 If successful, your commits should now be visible at:"
echo "https://github.com/jainamshah2028/enhanced-pdf-chat-app"
echo ""
echo "📊 Your GitHub profile will show:"
echo "- 1 new repository"
echo "- 1 commit today" 
echo "- 1,490+ lines of code added"
