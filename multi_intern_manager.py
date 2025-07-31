#!/usr/bin/env python3
"""
Multi-Intern Manager for AI Knowledge Assistant Internship Program
Manages individual intern branches and progressive assignment releases.
"""

import os
import sys
import subprocess
import json
from datetime import datetime, timedelta

class MultiInternManager:
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
        self.interns_file = "interns.json"
        self.load_interns()
        
    def load_interns(self):
        """Load intern data from JSON file"""
        if os.path.exists(self.interns_file):
            with open(self.interns_file, 'r') as f:
                self.interns = json.load(f)
        else:
            self.interns = {}
            self.save_interns()
    
    def save_interns(self):
        """Save intern data to JSON file"""
        with open(self.interns_file, 'w') as f:
            json.dump(self.interns, f, indent=2)
    
    def check_git_status(self):
        """Check if we're in a git repository"""
        try:
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Not in a git repository. Please run this from the project root.")
                return False
            return True
        except Exception as e:
            print(f"❌ Error checking git status: {e}")
            return False
    
    def add_intern(self, name, email, start_date=None):
        """Add a new intern to the program"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name in self.interns:
            print(f"❌ Intern {name} already exists!")
            return False
        
        self.interns[intern_name] = {
            "name": name,
            "email": email,
            "start_date": start_date or datetime.now().strftime("%Y-%m-%d"),
            "current_week": 1,
            "branch": f"intern-{intern_name}",
            "status": "active",
            "assignments_released": [1],
            "last_activity": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.save_interns()
        print(f"✅ Added intern: {name} ({intern_name})")
        print(f"📧 Email: {email}")
        print(f"🌿 Branch: intern-{intern_name}")
        
        return True
    
    def remove_intern(self, name):
        """Remove an intern from the program"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found!")
            return False
        
        intern = self.interns[intern_name]
        print(f"🗑️  Removing intern: {intern['name']}")
        print(f"📧 Email: {intern['email']}")
        print(f"🌿 Branch: {intern['branch']}")
        
        # Ask for confirmation
        confirm = input("Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            print("❌ Operation cancelled.")
            return False
        
        # Delete the branch
        try:
            subprocess.run(['git', 'branch', '-D', intern['branch']], check=True)
            subprocess.run(['git', 'push', 'origin', '--delete', intern['branch']], check=True)
            print(f"✅ Deleted branch: {intern['branch']}")
        except subprocess.CalledProcessError:
            print(f"⚠️  Could not delete branch: {intern['branch']}")
        
        # Remove from intern list
        del self.interns[intern_name]
        self.save_interns()
        
        print(f"✅ Removed intern: {name}")
        return True
    
    def list_interns(self):
        """List all interns and their status"""
        if not self.interns:
            print("📋 No interns registered.")
            return
        
        print("👥 Intern Status")
        print("=" * 80)
        print(f"{'Name':<20} {'Email':<25} {'Week':<5} {'Branch':<20} {'Status':<10}")
        print("-" * 80)
        
        for intern_name, intern in self.interns.items():
            print(f"{intern['name']:<20} {intern['email']:<25} {intern['current_week']:<5} {intern['branch']:<20} {intern['status']:<10}")
        
        print()
    
    def create_intern_branch(self, name):
        """Create a new branch for an intern"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found! Add them first.")
            return False
        
        intern = self.interns[intern_name]
        branch_name = intern['branch']
        
        try:
            # Create branch from main
            subprocess.run(['git', 'checkout', 'main'], check=True)
            subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
            
            # Push to remote
            subprocess.run(['git', 'push', 'origin', branch_name], check=True)
            
            print(f"✅ Created branch: {branch_name}")
            print(f"📧 Notify {intern['name']} to clone and checkout: {branch_name}")
            
            # Switch back to main
            subprocess.run(['git', 'checkout', 'main'], check=True)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating branch: {e}")
            return False
    
    def release_week_to_intern(self, week_number, name):
        """Release assignments for a specific week to a specific intern"""
        if week_number < 1 or week_number > 10:
            print("❌ Invalid week number. Must be between 1 and 10.")
            return False
        
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found! Add them first.")
            return False
        
        intern = self.interns[intern_name]
        week_folder = self.weeks[week_number - 1]
        branch_name = intern['branch']
        
        if not os.path.exists(week_folder):
            print(f"❌ Week folder '{week_folder}' not found.")
            return False
        
        print(f"🚀 Releasing Week {week_number} to {intern['name']} ({branch_name})")
        
        try:
            # Switch to intern branch
            subprocess.run(['git', 'checkout', branch_name], check=True)
            print(f"✅ Switched to branch: {branch_name}")
            
            # Unlock the week if it's locked
            backup_folder = f"{week_folder}_backup"
            if os.path.exists(backup_folder):
                self.unlock_week(week_number)
            
            # Add all changes
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit changes
            commit_message = f"Release Week {week_number} assignments to {intern['name']}"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print(f"✅ Committed changes: {commit_message}")
            
            # Push to remote
            subprocess.run(['git', 'push', 'origin', branch_name], check=True)
            print(f"✅ Pushed to remote: {branch_name}")
            
            # Update intern status
            intern['current_week'] = week_number
            intern['assignments_released'].append(week_number)
            intern['last_activity'] = datetime.now().strftime("%Y-%m-%d")
            self.save_interns()
            
            # Switch back to main
            subprocess.run(['git', 'checkout', 'main'], check=True)
            
            print(f"\n🎉 Week {week_number} assignments released to {intern['name']}!")
            print(f"📧 Notify {intern['name']} to run: git pull origin {branch_name}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error releasing week: {e}")
            # Switch back to main on error
            subprocess.run(['git', 'checkout', 'main'], check=True)
            return False
    
    def lock_future_weeks(self, current_week):
        """Lock future weeks by removing their content"""
        print(f"🔒 Locking future weeks (after week {current_week})...")
        
        for i in range(current_week, len(self.weeks)):
            week_folder = self.weeks[i]
            if os.path.exists(week_folder):
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
                
                # Save current content to backup
                backup_folder = f"{week_folder}_backup"
                if not os.path.exists(backup_folder):
                    os.rename(week_folder, backup_folder)
                
                # Create new folder with placeholder
                os.makedirs(week_folder, exist_ok=True)
                with open(f"{week_folder}/README.md", 'w', encoding='utf-8') as f:
                    f.write(placeholder_content)
                    
                print(f"✅ Locked {week_folder}")
    
    def unlock_week(self, week_number):
        """Unlock a specific week by restoring its content"""
        if week_number < 1 or week_number > 10:
            print("❌ Invalid week number. Must be between 1 and 10.")
            return False
        
        week_folder = self.weeks[week_number - 1]
        backup_folder = f"{week_folder}_backup"
        
        if not os.path.exists(backup_folder):
            print(f"❌ No backup found for {week_folder}")
            return False
        
        # Remove current placeholder
        if os.path.exists(week_folder):
            import shutil
            shutil.rmtree(week_folder)
        
        # Restore from backup
        os.rename(backup_folder, week_folder)
        print(f"✅ Unlocked {week_folder}")
        
        return True
    
    def show_status(self):
        """Show the status of all weeks"""
        print("📊 Assignment Release Status")
        print("=" * 50)
        
        for i, week in enumerate(self.weeks, 1):
            status = "🔒 Locked" if os.path.exists(f"{week}_backup") else "✅ Available"
            print(f"Week {i:2d}: {week:<20} {status}")
    
    def list_intern_branches(self):
        """List all intern branches"""
        try:
            result = subprocess.run(['git', 'branch', '-r'], capture_output=True, text=True)
            branches = result.stdout.strip().split('\n')
            intern_branches = [b.strip() for b in branches if 'origin/intern-' in b]
            
            print("🌿 Intern Branches")
            print("=" * 30)
            for branch in intern_branches:
                intern_name = branch.replace('origin/intern-', '')
                print(f"📁 {branch} ({intern_name})")
            
            if not intern_branches:
                print("No intern branches found.")
                
        except Exception as e:
            print(f"❌ Error listing branches: {e}")
    
    def create_release_notes(self, week_number, name):
        """Create release notes for a week"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found!")
            return False
        
        intern = self.interns[intern_name]
        week_folder = self.weeks[week_number - 1]
        
        release_notes = f"""# Week {week_number} Assignment Release - {intern['name']}

## 🎉 New Assignments Available!

Week {week_number} assignments have been released to your branch. Here's what's new:

### 📁 New Content
- `{week_folder}/` - Complete assignment materials
- Updated README with detailed instructions
- Starter code and resources
- Learning objectives and requirements

### 🚀 Getting Started

1. **Pull the latest changes from your branch:**
   ```bash
   git pull origin {intern['branch']}
   ```

2. **Create a feature branch for your work:**
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
        
        filename = f"release_notes_week_{week_number}_{intern_name}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(release_notes)
        
        print(f"✅ Created release notes: {filename}")
        return True
    
    def update_intern_progress(self, name, current_week):
        """Update intern's current week progress"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found!")
            return False
        
        self.interns[intern_name]['current_week'] = current_week
        self.interns[intern_name]['last_activity'] = datetime.now().strftime("%Y-%m-%d")
        self.save_interns()
        
        print(f"✅ Updated {name}'s progress to Week {current_week}")
        return True
    
    def get_intern_info(self, name):
        """Get detailed information about an intern"""
        intern_name = name.lower().replace(' ', '-')
        
        if intern_name not in self.interns:
            print(f"❌ Intern {name} not found!")
            return False
        
        intern = self.interns[intern_name]
        
        print(f"👤 Intern Information: {intern['name']}")
        print("=" * 50)
        print(f"📧 Email: {intern['email']}")
        print(f"📅 Start Date: {intern['start_date']}")
        print(f"📊 Current Week: {intern['current_week']}")
        print(f"🌿 Branch: {intern['branch']}")
        print(f"📈 Status: {intern['status']}")
        print(f"📋 Assignments Released: {intern['assignments_released']}")
        print(f"🕒 Last Activity: {intern['last_activity']}")
        
        return True

def main():
    manager = MultiInternManager()
    
    if len(sys.argv) < 2:
        print("Multi-Intern Manager for AI Knowledge Assistant Internship")
        print("=" * 60)
        print("Usage:")
        print("  python multi_intern_manager.py add <name> <email>              # Add new intern")
        print("  python multi_intern_manager.py remove <name>                   # Remove intern")
        print("  python multi_intern_manager.py list                           # List all interns")
        print("  python multi_intern_manager.py info <name>                     # Get intern info")
        print("  python multi_intern_manager.py create-branch <name>            # Create intern branch")
        print("  python multi_intern_manager.py release <week> <name>           # Release week to intern")
        print("  python multi_intern_manager.py lock <current_week>             # Lock future weeks")
        print("  python multi_intern_manager.py unlock <week>                   # Unlock a week")
        print("  python multi_intern_manager.py notes <week> <name>             # Create release notes")
        print("  python multi_intern_manager.py branches                        # List intern branches")
        print("  python multi_intern_manager.py status                          # Show week status")
        print("  python multi_intern_manager.py progress <name> <week>          # Update intern progress")
        return
    
    command = sys.argv[1]
    
    if not manager.check_git_status():
        return
    
    if command == "add":
        if len(sys.argv) < 4:
            print("❌ Please specify name and email")
            return
        name = sys.argv[2]
        email = sys.argv[3]
        manager.add_intern(name, email)
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("❌ Please specify intern name")
            return
        name = sys.argv[2]
        manager.remove_intern(name)
    
    elif command == "list":
        manager.list_interns()
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("❌ Please specify intern name")
            return
        name = sys.argv[2]
        manager.get_intern_info(name)
    
    elif command == "create-branch":
        if len(sys.argv) < 3:
            print("❌ Please specify intern name")
            return
        name = sys.argv[2]
        manager.create_intern_branch(name)
    
    elif command == "release":
        if len(sys.argv) < 4:
            print("❌ Please specify week number and intern name")
            return
        week_number = int(sys.argv[2])
        name = sys.argv[3]
        manager.release_week_to_intern(week_number, name)
    
    elif command == "lock":
        if len(sys.argv) < 3:
            print("❌ Please specify current week")
            return
        current_week = int(sys.argv[2])
        manager.lock_future_weeks(current_week)
    
    elif command == "unlock":
        if len(sys.argv) < 3:
            print("❌ Please specify week number")
            return
        week_number = int(sys.argv[2])
        manager.unlock_week(week_number)
    
    elif command == "notes":
        if len(sys.argv) < 4:
            print("❌ Please specify week number and intern name")
            return
        week_number = int(sys.argv[2])
        name = sys.argv[3]
        manager.create_release_notes(week_number, name)
    
    elif command == "branches":
        manager.list_intern_branches()
    
    elif command == "status":
        manager.show_status()
    
    elif command == "progress":
        if len(sys.argv) < 4:
            print("❌ Please specify intern name and current week")
            return
        name = sys.argv[2]
        current_week = int(sys.argv[3])
        manager.update_intern_progress(name, current_week)
    
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == "__main__":
    main() 