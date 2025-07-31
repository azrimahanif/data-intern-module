# Multi-Intern Setup Guide - Individual Branch Workflow

## 🎯 Welcome to the AI Knowledge Assistant Internship!

This guide explains how to work with your individual branch in the multi-intern system. Each intern has their own branch to work independently while learning proper Git workflow.

## 🚀 Initial Setup

### 1. Install Required Software

**Git:**
- **Windows:** Download from [git-scm.com](https://git-scm.com/)
- **Mac:** `brew install git`
- **Linux:** `sudo apt-get install git`

**Python 3.9+:**
- **Windows:** Download from [python.org](https://python.org/)
- **Mac:** `brew install python`
- **Linux:** `sudo apt-get install python3`

**VS Code (Recommended):**
- Download from [code.visualstudio.com](https://code.visualstudio.com/)
- Install Python extension

### 2. Configure Git

```bash
# Set your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default branch name
git config --global init.defaultBranch main
```

### 3. Clone and Set Up Your Branch

**Step 1: Clone the repository**
```bash
git clone <repository-url>
cd internship-auni-2025
```

**Step 2: Switch to your personal branch**
```bash
# Your mentor will tell you your branch name
# Example: intern-sarah, intern-john, etc.
git checkout intern-sarah  # Replace with your branch name
```

**Step 3: Verify you're on the right branch**
```bash
git branch
# Should show: * intern-sarah
```

## 📚 Git Workflow for Your Individual Branch

### **Getting New Assignments**

When your mentor releases new assignments to your branch:

1. **Pull the latest changes from your branch:**
   ```bash
   git pull origin intern-sarah  # Replace with your branch name
   ```

2. **Check what's new:**
   ```bash
   ls -la  # See new week folders
   ```

3. **Read the new assignment:**
   ```bash
   cd week2_etl  # Example: new week folder
   cat README.md  # Read assignment instructions
   ```

### **Working on Assignments**

1. **Create a feature branch for your work:**
   ```bash
   git checkout -b week2-assignment  # Create feature branch
   ```

2. **Work on assignments:**
   ```bash
   cd week2_etl/submission
   # Create your Python scripts, SQL files, etc.
   ```

3. **Commit your progress frequently:**
   ```bash
   git add .
   git commit -m "Week 2: ETL pipeline - data extraction completed"
   ```

4. **Push to your feature branch:**
   ```bash
   git push origin week2-assignment
   ```

### **Submitting Completed Work**

1. **Final commit:**
   ```bash
   git add .
   git commit -m "Week 2: ETL pipeline assignments completed"
   git push origin week2-assignment
   ```

2. **Merge back to your main branch (optional):**
   ```bash
   git checkout intern-sarah  # Switch to your main branch
   git merge week2-assignment  # Merge your work
   git push origin intern-sarah  # Push to your branch
   ```

3. **Clean up feature branch:**
   ```bash
   git branch -d week2-assignment  # Delete local feature branch
   git push origin --delete week2-assignment  # Delete remote feature branch
   ```

## 🔧 Common Git Commands for Your Workflow

### **Branch Management**
```bash
git branch                    # List local branches
git branch -r                 # List remote branches
git checkout branch-name      # Switch to branch
git checkout -b new-branch    # Create and switch to new branch
git branch -d branch-name     # Delete local branch
```

### **Working with Your Branch**
```bash
git pull origin intern-sarah  # Get updates from your branch
git push origin intern-sarah  # Push to your branch
git status                    # Check current status
git log --oneline            # See commit history
```

### **Feature Branch Workflow**
```bash
git checkout -b week-X-assignment  # Create feature branch
# Work on assignments
git add .
git commit -m "Progress: description"
git push origin week-X-assignment
git checkout intern-sarah           # Switch back to main branch
git merge week-X-assignment         # Merge when done
```

## 📋 Weekly Workflow Checklist

### **Monday (Assignment Release)**
- [ ] Receive notification from mentor
- [ ] Run `git pull origin intern-sarah` (your branch)
- [ ] Read new assignment README
- [ ] Create feature branch: `git checkout -b week-X-assignment`
- [ ] Plan your approach

### **Tuesday-Thursday (Development)**
- [ ] Work on assignments
- [ ] Commit frequently: `git commit -m "Progress: description"`
- [ ] Push to feature branch: `git push origin week-X-assignment`
- [ ] Ask questions in Slack if stuck

### **Friday (Submission)**
- [ ] Complete all assignments
- [ ] Test your code
- [ ] Update documentation
- [ ] Final commit: `git commit -m "Week X: All assignments completed"`
- [ ] Push to feature branch
- [ ] Merge to your main branch (optional)
- [ ] Submit via email/Slack

## 🆘 Troubleshooting

### **Common Issues**

**"Branch not found":**
```bash
# Make sure you're using the correct branch name
git branch -r  # List all remote branches
git checkout intern-sarah  # Use your specific branch name
```

**"Permission denied" when pushing:**
```bash
# Set up SSH key or use HTTPS
git remote set-url origin https://github.com/username/repo.git
```

**"Branch already exists":**
```bash
# Delete local branch and recreate
git branch -D week-X-assignment
git checkout -b week-X-assignment
```

**"Merge conflicts":**
```bash
# Resolve conflicts in your editor
# Then add and commit
git add .
git commit -m "Resolved merge conflicts"
```

**"Can't push to main":**
```bash
# You should never push to main - use your branch
git push origin intern-sarah  # Your branch
```

### **Getting Help**

- **Git Issues:** #git-support Slack channel
- **Assignment Questions:** #internship-assignments Slack channel
- **Office Hours:** Tuesdays 3-4 PM, Thursdays 2-4 PM
- **Email:** internship-support@company.com

## 📚 Learning Resources

### **Git Tutorials**
- [Git Handbook](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Git Branching](https://learngitbranching.js.org/)

### **Practice**
- [GitHub Learning Lab](https://lab.github.com/)
- [Git Exercises](https://gitexercises.fracz.com/)

## 🎯 Success Tips

1. **Always work on your branch** - Never push to main
2. **Use feature branches** - Keep your main branch clean
3. **Commit frequently** - Don't wait until the end
4. **Use descriptive commit messages** - Explain what you did
5. **Ask questions early** - Don't get stuck for too long
6. **Document your work** - Good documentation is part of the grade
7. **Test your code** - Make sure it works before submitting

## 🔄 Branch Structure Explained

### **Repository Structure:**
```
main (master)           → Week 1 only (template for new interns)
├── intern-sarah        → Week 1 + Week 2 + Week 3... (your progress)
├── intern-john         → Week 1 + Week 2... (other intern)
└── intern-emma         → Week 1 only (new intern)
```

### **Your Branch Contains:**
- **Week 1:** Always available (Python & SQL)
- **Week 2:** Released when you're ready
- **Week 3:** Released when you complete Week 2
- **And so on...**

### **Benefits:**
- ✅ **Independent progress** - Work at your own pace
- ✅ **No interference** - Other interns don't affect your work
- ✅ **Clean history** - Your commits are separate
- ✅ **Easy onboarding** - New interns start from main

## 📞 Contact Information

- **Mentor:** [Mentor Name] - mentor@company.com
- **Technical Lead:** [Tech Lead Name] - tech-lead@company.com
- **Program Coordinator:** coordinator@company.com

## 🚀 Quick Start Commands

```bash
# 1. Clone repository
git clone <repository-url>
cd internship-auni-2025

# 2. Switch to your branch (mentor will provide name)
git checkout intern-sarah  # Replace with your branch name

# 3. Verify you're on the right branch
git branch

# 4. Start Week 1
cd week1_python_sql
cat README.md

# 5. Create feature branch for work
git checkout -b week1-assignment
cd submission
# Start working on assignments!
```

---

**Remember:** You have your own branch to work independently. This teaches you real-world Git workflow while keeping your progress separate from other interns!

Good luck! 🚀 