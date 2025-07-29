# Assignment Release Schedule

## 📅 Progressive Assignment Release Plan

This document outlines the schedule for releasing assignments week by week, teaching proper Git workflow and project management.

## 🎯 Learning Objectives

- **Git Workflow**: Learn to pull, commit, push, and sync with remote repository
- **Project Management**: Understand progressive development and iteration
- **Version Control**: Practice proper branching and merging strategies
- **Collaboration**: Work with remote repositories and team workflows

## 📋 Release Schedule

### Week 1: Python & SQL Fundamentals
**Release Date:** Program Start  
**Status:** ✅ Available  
**Git Commands to Learn:**
```bash
git clone <repository-url>
git pull origin main
git add .
git commit -m "Week 1: Python & SQL assignments completed"
git push origin main
```

### Week 2: ETL Pipeline Development
**Release Date:** End of Week 1  
**Status:** 🔒 Locked (will be released)  
**Git Commands to Learn:**
```bash
git pull origin main  # Get new assignment
git checkout -b week2-etl  # Create feature branch
git add .
git commit -m "Week 2: ETL pipeline implementation"
git push origin week2-etl
git checkout main
git merge week2-etl
```

### Week 3: FastAPI Development
**Release Date:** End of Week 2  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week3-fastapi
# Work on assignments
git add .
git commit -m "Week 3: FastAPI development"
git push origin week3-fastapi
```

### Week 4: Docker & CI/CD
**Release Date:** End of Week 3  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week4-docker
# Work on assignments
git add .
git commit -m "Week 4: Docker and CI/CD implementation"
git push origin week4-docker
```

### Week 5: Vector Database Implementation
**Release Date:** End of Week 4  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week5-vector-db
# Work on assignments
git add .
git commit -m "Week 5: Vector database implementation"
git push origin week5-vector-db
```

### Week 6: RAG Pipeline Development
**Release Date:** End of Week 5  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week6-rag
# Work on assignments
git add .
git commit -m "Week 6: RAG pipeline development"
git push origin week6-rag
```

### Week 7: LLM Prompting Techniques
**Release Date:** End of Week 6  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week7-prompting
# Work on assignments
git add .
git commit -m "Week 7: LLM prompting techniques"
git push origin week7-prompting
```

### Week 8: AI Agent Development
**Release Date:** End of Week 7  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week8-ai-agent
# Work on assignments
git add .
git commit -m "Week 8: AI agent development"
git push origin week8-ai-agent
```

### Week 9: Capstone Project
**Release Date:** End of Week 8  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week9-capstone
# Work on assignments
git add .
git commit -m "Week 9: Capstone project integration"
git push origin week9-capstone
```

### Week 10: Final Presentation
**Release Date:** End of Week 9  
**Status:** 🔒 Locked  
**Git Commands to Learn:**
```bash
git pull origin main
git checkout -b week10-presentation
# Work on assignments
git add .
git commit -m "Week 10: Final presentation preparation"
git push origin week10-presentation
```

## 🔄 Release Process

### For Mentors/Instructors

1. **Prepare Next Week's Content**
   ```bash
   # Create new branch for next week
   git checkout -b release-week-X
   
   # Add new assignment content
   # Update README files
   # Add starter materials
   
   # Commit and push
   git add .
   git commit -m "Release Week X assignments"
   git push origin release-week-X
   
   # Merge to main
   git checkout main
   git merge release-week-X
   git push origin main
   ```

2. **Notify Intern**
   - Send email/Slack notification
   - Provide Git commands to run
   - Schedule review meeting

### For Interns

1. **Receive Notification**
   - Check email/Slack for new assignment
   - Review release notes

2. **Pull Latest Changes**
   ```bash
   git pull origin main
   ```

3. **Start New Assignment**
   ```bash
   git checkout -b week-X-assignment
   # Work on assignments
   ```

4. **Submit Work**
   ```bash
   git add .
   git commit -m "Week X: Assignment completed"
   git push origin week-X-assignment
   ```

## 📚 Git Learning Path

### Week 1-2: Basic Git Operations
- `git clone`, `git pull`, `git push`
- `git add`, `git commit`
- Basic branching

### Week 3-4: Intermediate Git
- Feature branches
- Merge strategies
- Conflict resolution

### Week 5-6: Advanced Git
- Rebase operations
- Stash and cherry-pick
- Git hooks

### Week 7-8: Collaboration
- Pull requests
- Code reviews
- Team workflows

### Week 9-10: Project Management
- Release management
- Version tagging
- Documentation

## 🎯 Success Metrics

### Git Proficiency
- [ ] Can pull latest assignments independently
- [ ] Uses proper commit messages
- [ ] Creates feature branches for work
- [ ] Handles merge conflicts
- [ ] Submits work via pull requests

### Project Management
- [ ] Follows release schedule
- [ ] Completes assignments on time
- [ ] Maintains clean repository history
- [ ] Documents progress properly

## 📞 Support & Communication

### Git Issues
- **Slack Channel:** #git-support
- **Office Hours:** Tuesdays, 3-4 PM
- **Documentation:** [Git Handbook](https://guides.github.com/)

### Assignment Questions
- **Slack Channel:** #internship-assignments
- **Email:** assignments@company.com
- **Office Hours:** Thursdays, 2-4 PM

---

**Remember**: This progressive release system is designed to teach both technical skills and professional development practices. Each week builds upon the previous, creating a comprehensive learning experience. 