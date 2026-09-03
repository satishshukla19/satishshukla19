#!/usr/bin/env python3
"""
Fetch today's commits from all repositories
"""
import os
import requests
import json
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_USER = os.environ.get('GITHUB_ACTOR', 'satishshukla19')

def get_today_commits():
    """Fetch commits made today"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get today's date range
    today = datetime.utcnow()
    start_date = today.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    end_date = (today + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
    
    # Search for commits
    query = f'author:{GITHUB_USER} committer-date:{start_date}..{end_date}'
    url = f'https://api.github.com/search/commits?q={query}&sort=committer-date&order=desc&per_page=100'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        commits = data.get('items', [])
        total_count = data.get('total_count', 0)
        
        # Get repository info from commits
        repo_commits = {}
        for commit in commits:
            repo = commit['repository']['full_name']
            if repo not in repo_commits:
                repo_commits[repo] = []
            repo_commits[repo].append(commit)
        
        # Find most active repo (today)
        active_repo = max(repo_commits, key=lambda r: len(repo_commits[r])) if repo_commits else 'Unknown'
        
        # Format commit messages
        commit_messages = []
        for commit in commits[:5]:  # Top 5 commits
            msg = commit['commit']['message'].split('\n')[0][:60]
            commit_messages.append(msg)
        
        return {
            'commit_count': total_count,
            'active_repo': active_repo,
            'commit_messages': commit_messages,
            'repo_commits': repo_commits
        }
    except Exception as e:
        print(f"Error fetching commits: {e}")
        return {
            'commit_count': 0,
            'active_repo': 'Unknown',
            'commit_messages': [],
            'repo_commits': {}
        }

if __name__ == '__main__':
    result = get_today_commits()
    
    # Output as GitHub Actions environment variables
    with open(os.environ.get('GITHUB_OUTPUT', '/tmp/github_output.txt'), 'a') as f:
        f.write(f"commit_count={result['commit_count']}\n")
        f.write(f"active_repo={result['active_repo']}\n")
        f.write(f"commit_messages={json.dumps(result['commit_messages'])}\n")
    
    print(f"Found {result['commit_count']} commits today")
    print(f"Most active repo: {result['active_repo']}")
