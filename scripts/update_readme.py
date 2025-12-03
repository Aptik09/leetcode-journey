#!/usr/bin/env python3
"""
README Update Script
Automatically updates README with latest stats and calendar
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
STATS_DIR = BASE_DIR / "stats"
PROBLEMS_DIR = BASE_DIR / "problems"
README_PATH = BASE_DIR / "README.md"


class ReadmeUpdater:
    def __init__(self):
        self.stats = self.load_stats()
        self.problems = self.scan_problems()
        self.calendar_data = self.load_calendar()
    
    def load_stats(self):
        """Load statistics"""
        stats_file = STATS_DIR / "progress.json"
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                return json.load(f)
        return {
            "total_solved": 0,
            "easy_solved": 0,
            "medium_solved": 0,
            "hard_solved": 0,
            "ranking": 0
        }
    
    def load_calendar(self):
        """Load calendar data"""
        calendar_file = STATS_DIR / "calendar.json"
        if calendar_file.exists():
            with open(calendar_file, 'r') as f:
                return json.load(f)
        return {}
    
    def scan_problems(self):
        """Scan all solved problems"""
        problems = {
            "easy": defaultdict(list),
            "medium": defaultdict(list),
            "hard": defaultdict(list)
        }
        
        for difficulty in ["easy", "medium", "hard"]:
            diff_dir = PROBLEMS_DIR / difficulty
            if not diff_dir.exists():
                continue
            
            for topic_dir in diff_dir.iterdir():
                if not topic_dir.is_dir():
                    continue
                
                topic = topic_dir.name
                for problem_file in topic_dir.glob("*.md"):
                    problems[difficulty][topic].append(problem_file)
        
        return problems
    
    def calculate_streak(self):
        """Calculate current streak"""
        if not self.calendar_data:
            return 0
        
        dates = sorted(self.calendar_data.keys(), reverse=True)
        if not dates:
            return 0
        
        today = datetime.now().date()
        streak = 0
        
        for date_str in dates:
            date = datetime.fromisoformat(date_str).date()
            expected_date = today - timedelta(days=streak)
            
            if date == expected_date:
                streak += 1
            else:
                break
        
        return streak
    
    def generate_calendar(self, year, month):
        """Generate calendar for a specific month"""
        import calendar
        
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # Header
        calendar_str = f"### {month_name} {year}\n```\n"
        calendar_str += "Sun Mon Tue Wed Thu Fri Sat\n"
        
        # Days
        for week in cal:
            week_str = ""
            for day in week:
                if day == 0:
                    week_str += "    "
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    if date_str in self.calendar_data:
                        week_str += f" ✅ "
                    else:
                        week_str += f"{day:3d} "
            calendar_str += week_str + "\n"
        
        calendar_str += "```\n"
        return calendar_str
    
    def generate_topic_section(self, topic, problems_list):
        """Generate topic section"""
        section = f"""<details>
<summary>📚 <b>{topic.replace('-', ' ').title()}</b> ({len(problems_list)} problems)</summary>

| # | Problem | Difficulty | Solution | Date |
|---|---------|-----------|----------|------|
"""
        
        for problem_file in sorted(problems_list):
            # Parse problem file
            with open(problem_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract info (simplified)
            lines = content.split('\n')
            title_line = lines[0].replace('#', '').strip()
            
            # Extract problem number and title
            parts = title_line.split('.', 1)
            if len(parts) == 2:
                number = parts[0].strip()
                title = parts[1].strip()
            else:
                number = "?"
                title = title_line
            
            # Get difficulty from file path
            difficulty = problem_file.parent.parent.name.capitalize()
            difficulty_emoji = {
                "Easy": "🟢",
                "Medium": "🟡",
                "Hard": "🔴"
            }.get(difficulty, "⚪")
            
            # Get date (from file modification time)
            date = datetime.fromtimestamp(problem_file.stat().st_mtime).strftime('%Y-%m-%d')
            
            # Relative path for link
            rel_path = problem_file.relative_to(BASE_DIR)
            
            section += f"| {number} | [{title}]({rel_path}) | {difficulty_emoji} {difficulty} | [View]({rel_path}) | {date} |\n"
        
        section += "\n</details>\n\n"
        return section
    
    def generate_readme(self):
        """Generate complete README"""
        streak = self.calculate_streak()
        total = self.stats['total_solved']
        
        readme = f"""# 🚀 LeetCode Journey - Aptik Pandey

<div align="center">

![LeetCode Stats](https://leetcard.jacoblin.cool/aptikpandey9?theme=dark&font=Ubuntu&ext=contest)

[![Profile](https://img.shields.io/badge/LeetCode-Profile-orange?style=for-the-badge&logo=leetcode)](https://leetcode.com/u/aptikpandey9/)
[![Streak](https://img.shields.io/badge/Current_Streak-{streak}_days-success?style=for-the-badge)](https://github.com/Aptik09/leetcode-journey)
[![Problems Solved](https://img.shields.io/badge/Problems_Solved-{total}-blue?style=for-the-badge)](https://github.com/Aptik09/leetcode-journey)

</div>

---

## 📊 Progress Dashboard

### 🔥 Current Streak: **{streak} Days**
### 📈 Total Problems Solved: **{total}**
### 🎯 This Month: **{len(self.calendar_data)} Problems**

---

## 📅 2025 Coding Calendar (Atomic Habits Style)

"""
        
        # Add calendar for current month
        now = datetime.now()
        readme += self.generate_calendar(now.year, now.month)
        
        readme += """
**Legend:** ✅ = Solved | 🔥 = Streak Day | 🏆 = Contest Day

---

## 🎯 Problem Statistics

| Difficulty | Solved | Total | Percentage |
|-----------|--------|-------|------------|
"""
        
        easy_pct = (self.stats['easy_solved'] / 826 * 100) if self.stats['easy_solved'] > 0 else 0
        medium_pct = (self.stats['medium_solved'] / 1739 * 100) if self.stats['medium_solved'] > 0 else 0
        hard_pct = (self.stats['hard_solved'] / 753 * 100) if self.stats['hard_solved'] > 0 else 0
        total_pct = (total / 3318 * 100) if total > 0 else 0
        
        readme += f"| 🟢 Easy | {self.stats['easy_solved']} | 826 | {easy_pct:.1f}% |\n"
        readme += f"| 🟡 Medium | {self.stats['medium_solved']} | 1739 | {medium_pct:.1f}% |\n"
        readme += f"| 🔴 Hard | {self.stats['hard_solved']} | 753 | {hard_pct:.1f}% |\n"
        readme += f"| **Total** | **{total}** | **3318** | **{total_pct:.1f}%** |\n"
        
        readme += "\n---\n\n## 📚 Topics Mastered\n\n"
        
        # Add topic sections
        all_topics = set()
        for difficulty in ["easy", "medium", "hard"]:
            all_topics.update(self.problems[difficulty].keys())
        
        for topic in sorted(all_topics):
            # Combine problems from all difficulties
            all_problems = []
            for difficulty in ["easy", "medium", "hard"]:
                all_problems.extend(self.problems[difficulty].get(topic, []))
            
            if all_problems:
                readme += self.generate_topic_section(topic, all_problems)
        
        readme += """
---

## 🏆 Contest Performance

### Weekly Contests
| Contest | Rank | Score | Problems Solved | Date |
|---------|------|-------|----------------|------|
| - | - | - | - | - |

### Biweekly Contests
| Contest | Rank | Score | Problems Solved | Date |
|---------|------|-------|----------------|------|
| - | - | - | - | - |

---

## 📁 Repository Structure

```
leetcode-journey/
├── README.md                          # This file
├── problems/                          # All solved problems
│   ├── easy/                         # Easy problems
│   ├── medium/                       # Medium problems
│   └── hard/                         # Hard problems
├── contests/                         # Contest solutions
├── scripts/                          # Automation scripts
└── stats/                            # Statistics and tracking
```

---

## 🛠️ How It Works

This repository automatically syncs with my LeetCode profile:

1. **Auto-Sync**: When I solve a problem on LeetCode, it automatically gets added here
2. **Organization**: Problems are organized by difficulty and topic
3. **Calendar**: Atomic habits-style calendar tracks daily progress
4. **Stats**: Real-time statistics and streak tracking
5. **Contests**: Weekly and biweekly contest performance tracking

---

## 🎯 Goals

- [ ] Solve 100 problems
- [ ] Maintain 30-day streak
- [ ] Master all Array problems
- [ ] Complete 10 contests
- [ ] Solve 50 Medium problems
- [ ] Solve 10 Hard problems

---

## 🤝 Connect With Me

[![LeetCode](https://img.shields.io/badge/LeetCode-aptikpandey9-orange?style=flat&logo=leetcode)](https://leetcode.com/u/aptikpandey9/)
[![GitHub](https://img.shields.io/badge/GitHub-Aptik09-black?style=flat&logo=github)](https://github.com/Aptik09)

---

<div align="center">

**"The only way to do great work is to love what you do."** - Steve Jobs

Made with ❤️ by Aptik Pandey | Last Updated: {datetime.now().strftime('%B %d, %Y')}

</div>
"""
        
        return readme
    
    def update(self):
        """Update README file"""
        print("📝 Updating README...")
        
        readme_content = self.generate_readme()
        
        with open(README_PATH, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ README updated successfully!")


def main():
    """Main entry point"""
    updater = ReadmeUpdater()
    updater.update()


if __name__ == "__main__":
    main()
