#!/usr/bin/env python3
"""
LeetCode Auto-Sync Script
Automatically syncs your LeetCode submissions to GitHub
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import time

# Configuration
LEETCODE_USERNAME = "aptikpandey9"
LEETCODE_API = "https://leetcode.com/graphql"
GITHUB_REPO = "Aptik09/leetcode-journey"

# Directories
BASE_DIR = Path(__file__).parent.parent
PROBLEMS_DIR = BASE_DIR / "problems"
STATS_DIR = BASE_DIR / "stats"
CONTESTS_DIR = BASE_DIR / "contests"

# Create directories
for dir_path in [PROBLEMS_DIR, STATS_DIR, CONTESTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Topic mapping
TOPIC_MAPPING = {
    "array": "Array",
    "string": "String",
    "hash-table": "Hash Table",
    "dynamic-programming": "Dynamic Programming",
    "math": "Math",
    "sorting": "Sorting",
    "greedy": "Greedy",
    "depth-first-search": "DFS",
    "breadth-first-search": "BFS",
    "binary-search": "Binary Search",
    "tree": "Tree",
    "matrix": "Matrix",
    "bit-manipulation": "Bit Manipulation",
    "two-pointers": "Two Pointers",
    "binary-tree": "Binary Tree",
    "heap": "Heap",
    "stack": "Stack",
    "graph": "Graph",
    "linked-list": "Linked List",
    "backtracking": "Backtracking",
}


class LeetCodeSync:
    def __init__(self):
        self.username = LEETCODE_USERNAME
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        })
    
    def get_user_profile(self):
        """Fetch user profile data"""
        query = """
        query getUserProfile($username: String!) {
            matchedUser(username: $username) {
                username
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                profile {
                    ranking
                    reputation
                }
            }
        }
        """
        
        variables = {"username": self.username}
        response = self.session.post(
            LEETCODE_API,
            json={"query": query, "variables": variables}
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_recent_submissions(self, limit=20):
        """Fetch recent AC submissions"""
        query = """
        query getRecentSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
                statusDisplay
                lang
            }
        }
        """
        
        variables = {"username": self.username, "limit": limit}
        response = self.session.post(
            LEETCODE_API,
            json={"query": query, "variables": variables}
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_problem_details(self, title_slug):
        """Fetch problem details"""
        query = """
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                content
                difficulty
                topicTags {
                    name
                    slug
                }
                codeSnippets {
                    lang
                    code
                }
                stats
            }
        }
        """
        
        variables = {"titleSlug": title_slug}
        response = self.session.post(
            LEETCODE_API,
            json={"query": query, "variables": variables}
        )
        
        if response.status_code == 200:
            return response.json()
        return None
    
    def save_problem(self, problem_data, submission_data):
        """Save problem to appropriate directory"""
        difficulty = problem_data['difficulty'].lower()
        topics = [tag['slug'] for tag in problem_data['topicTags']]
        primary_topic = topics[0] if topics else 'miscellaneous'
        
        # Create directory structure
        problem_dir = PROBLEMS_DIR / difficulty / primary_topic
        problem_dir.mkdir(parents=True, exist_ok=True)
        
        # Create problem file
        problem_id = problem_data['questionId']
        title_slug = problem_data['titleSlug']
        filename = f"{problem_id}_{title_slug}.md"
        filepath = problem_dir / filename
        
        # Generate markdown content
        content = self.generate_problem_markdown(problem_data, submission_data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Saved: {problem_data['title']}")
        return filepath
    
    def generate_problem_markdown(self, problem, submission):
        """Generate markdown for problem"""
        topics_str = ", ".join([tag['name'] for tag in problem['topicTags']])
        
        markdown = f"""# {problem['questionId']}. {problem['title']}

**Difficulty:** {problem['difficulty']}  
**Topics:** {topics_str}  
**Link:** [LeetCode](https://leetcode.com/problems/{problem['titleSlug']}/)  
**Solved:** {datetime.fromtimestamp(int(submission['timestamp'])).strftime('%Y-%m-%d %H:%M:%S')}

---

## Problem Statement

{problem['content']}

---

## Solution

```{submission['lang']}
// Solution will be added here
// Language: {submission['lang']}
```

---

## Complexity Analysis

- **Time Complexity:** O(?)
- **Space Complexity:** O(?)

---

## Notes

Add your notes here...

---

## Related Problems

- Problem 1
- Problem 2

"""
        return markdown
    
    def update_stats(self):
        """Update statistics file"""
        profile = self.get_user_profile()
        if not profile:
            return
        
        stats = {
            "last_updated": datetime.now().isoformat(),
            "username": self.username,
            "total_solved": 0,
            "easy_solved": 0,
            "medium_solved": 0,
            "hard_solved": 0,
            "ranking": profile['data']['matchedUser']['profile']['ranking']
        }
        
        for item in profile['data']['matchedUser']['submitStats']['acSubmissionNum']:
            difficulty = item['difficulty']
            count = item['count']
            
            if difficulty == "All":
                stats['total_solved'] = count
            elif difficulty == "Easy":
                stats['easy_solved'] = count
            elif difficulty == "Medium":
                stats['medium_solved'] = count
            elif difficulty == "Hard":
                stats['hard_solved'] = count
        
        # Save stats
        stats_file = STATS_DIR / "progress.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        print(f"📊 Stats updated: {stats['total_solved']} problems solved")
        return stats
    
    def sync(self):
        """Main sync function"""
        print("🔄 Starting LeetCode sync...")
        
        # Get recent submissions
        submissions = self.get_recent_submissions(limit=20)
        if not submissions:
            print("❌ Failed to fetch submissions")
            return
        
        submission_list = submissions['data']['recentAcSubmissionList']
        print(f"📥 Found {len(submission_list)} recent submissions")
        
        # Process each submission
        for submission in submission_list:
            title_slug = submission['titleSlug']
            
            # Get problem details
            problem_data = self.get_problem_details(title_slug)
            if not problem_data:
                continue
            
            problem = problem_data['data']['question']
            
            # Save problem
            self.save_problem(problem, submission)
            
            # Rate limiting
            time.sleep(1)
        
        # Update stats
        self.update_stats()
        
        print("✅ Sync completed!")


def main():
    """Main entry point"""
    syncer = LeetCodeSync()
    syncer.sync()


if __name__ == "__main__":
    main()
