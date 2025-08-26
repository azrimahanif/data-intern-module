#!/usr/bin/env python3
"""
Script to manage progressive assignment releases for the internship program.
This helps mentors release assignments week by week, teaching proper Git workflow.
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime, timedelta

class AssignmentReleaser:
    def __init__(self):
        self.weeks = [
            "week1_python_sql",
            "week2_etl", 
            "week3_api_fastapi",
            "week4_docker_ci",
            "week5_vector_db",
            "week6_rag_pipeline",
            "week7_prompting_llm",
            "week8_ai_agent",
            "week9_capstone",
            "week10_presentation"
        ]
        
        # Create secure backup directory (hidden from interns)
        self.secure_backup_dir = ".secure_assignments"
        
    def check_git_status(self):
        """Check if we're in a git repository and on main branch"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Not in a git repository. Please run this from the project root.")
                return False
                
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True)
            current_branch = result.stdout.strip()
            if current_branch != 'main':
                print(f"⚠️  Currently on branch '{current_branch}'. Switching to main...")
                subprocess.run(['git', 'checkout', 'main'])
                
            return True
        except Exception as e:
            print(f"❌ Error checking git status: {e}")
            return False
    
    def setup_secure_backups(self):
        """Set up secure backup system to prevent interns from seeing future weeks"""
        if not os.path.exists(self.secure_backup_dir):
            os.makedirs(self.secure_backup_dir)
            print(f"✅ Created secure backup directory: {self.secure_backup_dir}")
            
        # Move all backup folders to secure location
        for week in self.weeks:
            backup_folder = f"{week}_backup"
            if os.path.exists(backup_folder):
                secure_path = os.path.join(self.secure_backup_dir, f"{week}_backup")
                if not os.path.exists(secure_path):
                    shutil.move(backup_folder, secure_path)
                    print(f"✅ Moved {backup_folder} to secure location")
    
    def release_week(self, week_number):
        """Release assignments for a specific week"""
        if week_number < 1 or week_number > 10:
            print("❌ Invalid week number. Must be between 1 and 10.")
            return False
            
        week_folder = self.weeks[week_number - 1]
        
        if not os.path.exists(week_folder):
            print(f"❌ Week folder '{week_folder}' not found.")
            return False
            
        print(f"🚀 Releasing Week {week_number}: {week_folder}")
        
        # Create release branch
        release_branch = f"release-week-{week_number}"
        try:
            subprocess.run(['git', 'checkout', '-b', release_branch], check=True)
            print(f"✅ Created branch: {release_branch}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Branch {release_branch} already exists. Switching to it...")
            subprocess.run(['git', 'checkout', release_branch])
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit changes
        commit_message = f"Release Week {week_number} assignments"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        print(f"✅ Committed changes: {commit_message}")
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', release_branch], check=True)
        print(f"✅ Pushed to remote: {release_branch}")
        
        # Switch back to main
        subprocess.run(['git', 'checkout', 'main'], check=True)
        
        # Merge release branch
        subprocess.run(['git', 'merge', release_branch], check=True)
        print(f"✅ Merged {release_branch} into main")
        
        # Push main
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print(f"✅ Pushed main branch")
        
        # Clean up release branch
        subprocess.run(['git', 'branch', '-d', release_branch], check=True)
        subprocess.run(['git', 'push', 'origin', '--delete', release_branch], check=True)
        print(f"✅ Cleaned up {release_branch}")
        
        print(f"\n🎉 Week {week_number} assignments released successfully!")
        print(f"📧 Notify the intern to run: git pull origin main")
        
        return True
        
    def lock_future_weeks(self, current_week):
        """Lock future weeks by removing their content and storing securely"""
        print(f"🔒 Locking future weeks (after week {current_week})...")
        
        # Ensure secure backup directory exists
        self.setup_secure_backups()
        
        for i in range(current_week, len(self.weeks)):
            week_folder = self.weeks[i]
            if os.path.exists(week_folder):
                # Check if content exists (not just placeholder)
                readme_path = os.path.join(week_folder, "README.md")
                if os.path.exists(readme_path):
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if "Assignment Locked" not in content:
                            # This has real content, backup it securely
                            secure_path = os.path.join(self.secure_backup_dir, f"{week_folder}_backup")
                            if not os.path.exists(secure_path):
                                shutil.copytree(week_folder, secure_path)
                                print(f"✅ Backed up {week_folder} to secure location")
                
                # Create a placeholder README
                placeholder_content = f"""# Week {i+1}: {week_folder.replace('_', ' ').title()}

## 🔒 Assignment Locked

This week's assignments will be released at the end of Week {i}.

### What to expect:
- Detailed assignment instructions
- Starter code and resources
- Learning objectives
- Submission guidelines

### Git Commands to learn this week:
```bash
git pull origin main  # Get new assignments
git checkout -b week{i+1}-assignment  # Create feature branch
# Work on assignments
git add .
git commit -m "Week {i+1}: Assignment completed"
git push origin week{i+1}-assignment
```

Stay tuned for the release! 🚀
"""
                
                # Remove current content and create placeholder
                shutil.rmtree(week_folder)
                os.makedirs(week_folder, exist_ok=True)
                with open(f"{week_folder}/README.md", 'w', encoding='utf-8') as f:
                    f.write(placeholder_content)
                    
                print(f"✅ Locked {week_folder}")
    
    def unlock_week(self, week_number):
        """Unlock a specific week by restoring its content from secure backup"""
        if week_number < 1 or week_number > 10:
            print("❌ Invalid week number. Must be between 1 and 10.")
            return False
            
        week_folder = self.weeks[week_number - 1]
        secure_backup_path = os.path.join(self.secure_backup_dir, f"{week_folder}_backup")
        
        if not os.path.exists(secure_backup_path):
            print(f"❌ No secure backup found for {week_folder}")
            return False
            
        # Remove current placeholder
        if os.path.exists(week_folder):
            shutil.rmtree(week_folder)
        
        # Restore from secure backup
        shutil.copytree(secure_backup_path, week_folder)
        print(f"✅ Unlocked {week_folder} from secure backup")
        
        return True
    
    def show_status(self):
        """Show the status of all weeks"""
        print("📊 Assignment Release Status")
        print("=" * 50)
        
        for i, week in enumerate(self.weeks, 1):
            secure_backup_path = os.path.join(self.secure_backup_dir, f"{week}_backup")
            status = "🔒 Locked" if os.path.exists(secure_backup_path) else "✅ Available"
            print(f"Week {i:2d}: {week:<20} {status}")
    
    def create_release_notes(self, week_number):
        """Create release notes for a week"""
        week_folder = self.weeks[week_number - 1]
        
        release_notes = f"""# Week {week_number} Assignment Release

## 🎉 New Assignments Available!

Week {week_number} assignments have been released. Here's what's new:

### 📁 New Content
- `{week_folder}/` - Complete assignment materials
- Updated README with detailed instructions
- Starter code and resources
- Learning objectives and requirements

### 🚀 Getting Started

1. **Pull the latest changes:**
   ```bash
   git pull origin main
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b week{week_number}-assignment
   ```

3. **Start working on assignments:**
   - Read the README in `{week_folder}/`
   - Complete all required tasks
   - Follow submission guidelines

4. **Submit your work:**
   ```bash
   git add .
   git commit -m "Week {week_number}: Assignment completed"
   git push origin week{week_number}-assignment
   ```

### 📅 Due Date
**Friday, 5:00 PM** - Week {week_number} assignments due

### 📞 Support
- **Slack:** #internship-assignments
- **Office Hours:** Thursdays, 2-4 PM
- **Email:** assignments@company.com

Good luck! 🚀
"""
        
        filename = f"release_notes_week_{week_number}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(release_notes)
        
        print(f"✅ Created release notes: {filename}")

def main():
    releaser = AssignmentReleaser()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python release_assignments.py status                    # Show status")
        print("  python release_assignments.py release <week_number>     # Release a week")
        print("  python release_assignments.py lock <current_week>       # Lock future weeks")
        print("  python release_assignments.py unlock <week_number>      # Unlock a week")
        print("  python release_assignments.py notes <week_number>       # Create release notes")
        print("  python release_assignments.py secure                   # Set up secure backup system")
        return
    
    command = sys.argv[1]
    
    if not releaser.check_git_status():
        return
    
    if command == "status":
        releaser.show_status()
    
    elif command == "release":
        if len(sys.argv) < 3:
            print("❌ Please specify week number")
            return
        week_number = int(sys.argv[2])
        releaser.release_week(week_number)
    
    elif command == "lock":
        if len(sys.argv) < 3:
            print("❌ Please specify current week")
            return
        current_week = int(sys.argv[2])
        releaser.lock_future_weeks(current_week)
    
    elif command == "unlock":
        if len(sys.argv) < 3:
            print("❌ Please specify week number")
            return
        week_number = int(sys.argv[2])
        releaser.unlock_week(week_number)
    
    elif command == "notes":
        if len(sys.argv) < 3:
            print("❌ Please specify week number")
            return
        week_number = int(sys.argv[2])
        releaser.create_release_notes(week_number)
    
    elif command == "secure":
        releaser.setup_secure_backups()
        print("✅ Secure backup system initialized")
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main() 