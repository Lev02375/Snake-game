#!/bin/bash
# Push Snake Game to GitHub
# Run this script after creating a GitHub repository

# Configure git (if not already done)
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# Add remote if not exists
git remote add origin https://github.com/YOUR_USERNAME/snake-game.git 2>/dev/null || true

# Set the remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/snake-game.git

# Push to GitHub
git push -u origin main

echo "Done! Visit https://github.com/YOUR_USERNAME/snake-game to see your repository"