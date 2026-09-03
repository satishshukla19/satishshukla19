#!/usr/bin/env python3
"""
Update README.md with today's commit statistics
"""
import os
import json
import re
from datetime import datetime

COMMIT_COUNT = os.environ.get('COMMIT_COUNT', '0')
ACTIVE_REPO = os.environ.get('ACTIVE_REPO', 'Unknown')
COMMIT_MESSAGES_STR = os.environ.get('COMMIT_MESSAGES', '[]')

try:
    COMMIT_MESSAGES = json.loads(COMMIT_MESSAGES_STR)
except:
    COMMIT_MESSAGES = []

def update_readme():
    """Update README with today's stats"""
    with open('README.md', 'r') as f:
        content = f.read()
    
    today = datetime.utcnow().strftime('%b %d, %Y')
    
    # Create updated activity section
    activity_section = f"""## 📊 Today's Activity ({today})

- **Today's Commits:** {COMMIT_COUNT} contributions
- **Active Repository:** {ACTIVE_REPO}
- **Focus:** Development & Deployment Updates
- **Last Updated:** {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}"""
    
    # Find and replace the activity section
    pattern = r'## 📊 Today\'s Activity \(.*?\)\n\n.*?(?=\n---)'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, activity_section, content, flags=re.DOTALL)
    else:
        # If section doesn't exist, add it after "About Me"
        about_pattern = r'(## 🚀 About Me\n\n.*?\n---)'
        if re.search(about_pattern, content, re.DOTALL):
            content = re.sub(about_pattern, r'\1\n\n' + activity_section, content, flags=re.DOTALL)
    
    with open('README.md', 'w') as f:
        f.write(content)
    
    print("✅ README updated successfully!")

if __name__ == '__main__':
    update_readme()
