# Intern Setup Guide - Git Workflow

## 🎯 Welcome to the AI Knowledge Assistant Internship!

This guide will help you set up your development environment and learn the Git workflow for receiving assignments week by week.

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

### 3. Clone the Repository

```bash
# Clone the internship repository
git clone <repository-url>
cd internship-auni-2025

# Verify you're on the main branch
git branch
```

## 📚 Git Workflow for Weekly Assignments

### Week 1: Basic Git Operations

**When you receive notification that Week 1 is available:**

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Navigate to Week 1 folder:**
   ```bash
   cd week1_python_sql
   ```

3. **Read the assignment:**
   ```bash
   # Open README.md to understand requirements
   code README.md  # or use your preferred editor
   ```

4. **Work on assignments in the submission folder:**
   ```bash
   cd submission
   # Create your Python scripts, SQL files, etc.
   ```

5. **Submit your work:**
   ```bash
   # Add all your files
   git add .
   
   # Commit with a descriptive message
   git commit -m "Week 1: Python & SQL assignments completed"
   
   # Push to main branch
   git push origin main
   ```

### Week 2+: Advanced Git Workflow

**When you receive notification that a new week is available:**

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Create a feature branch for your work:**
   ```bash
   git checkout -b week2-etl  # Replace with current week
   ```

3. **Work on assignments:**
   ```bash
   cd week2_etl/submission
   # Complete your assignments
   ```

4. **Submit your work:**
   ```bash
   # Add all your files
   git add .
   
   # Commit with a descriptive message
   git commit -m "Week 2: ETL pipeline implementation"
   
   # Push your feature branch
   git push origin week2-etl
   ```

5. **Merge back to main (optional):**
   ```bash
   git checkout main
   git merge week2-etl
   git push origin main
   ```

## 🔧 Common Git Commands

### Basic Operations
```bash
git status                    # Check current status
git add .                     # Add all changes
git add filename.py           # Add specific file
git commit -m "Message"       # Commit changes
git push origin branch-name   # Push to remote
git pull origin branch-name   # Pull from remote
```

### Branching
```bash
git branch                    # List branches
git branch branch-name        # Create new branch
git checkout branch-name      # Switch to branch
git checkout -b branch-name   # Create and switch to branch
git merge branch-name         # Merge branch into current
```

### Information
```bash
git log                       # View commit history
git log --oneline            # Compact commit history
git diff                      # See changes
git diff filename.py          # See changes in specific file
```

## 📋 Weekly Workflow Checklist

### Monday (Assignment Release)
- [ ] Receive notification email/Slack
- [ ] Run `git pull origin main`
- [ ] Read new assignment README
- [ ] Create feature branch: `git checkout -b week-X-assignment`
- [ ] Plan your approach

### Tuesday-Thursday (Development)
- [ ] Work on assignments
- [ ] Commit frequently: `git commit -m "Progress: description"`
- [ ] Push to feature branch: `git push origin week-X-assignment`
- [ ] Ask questions in Slack if stuck

### Friday (Submission)
- [ ] Complete all assignments
- [ ] Test your code
- [ ] Update documentation
- [ ] Final commit: `git commit -m "Week X: All assignments completed"`
- [ ] Push to feature branch
- [ ] Merge to main (optional)
- [ ] Submit via email/Slack

## 🆘 Troubleshooting

### Common Issues

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
# Use feature branches instead
git checkout -b week-X-assignment
git push origin week-X-assignment
```

### Getting Help

- **Git Issues:** #git-support Slack channel
- **Assignment Questions:** #internship-assignments Slack channel
- **Office Hours:** Tuesdays 3-4 PM, Thursdays 2-4 PM
- **Email:** internship-support@company.com

## 📚 Learning Resources

### Git Tutorials
- [Git Handbook](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Git Branching](https://learngitbranching.js.org/)

### Practice
- [GitHub Learning Lab](https://lab.github.com/)
- [Git Exercises](https://gitexercises.fracz.com/)

## 🎯 Success Tips

1. **Commit frequently** - Don't wait until the end
2. **Use descriptive commit messages** - Explain what you did
3. **Create feature branches** - Keep main branch clean
4. **Ask questions early** - Don't get stuck for too long
5. **Document your work** - Good documentation is part of the grade
6. **Test your code** - Make sure it works before submitting

## 📞 Contact Information

- **Mentor:** [Mentor Name] - mentor@company.com
- **Technical Lead:** [Tech Lead Name] - tech-lead@company.com
- **Program Coordinator:** coordinator@company.com

---

**Remember:** Git is a powerful tool that will serve you throughout your career. Take the time to learn it well during this internship!

Good luck! 🚀 