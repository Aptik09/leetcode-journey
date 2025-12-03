# 🚀 Setup Guide - LeetCode Journey

This guide will help you set up automatic syncing between your LeetCode account and this GitHub repository.

---

## 📋 Prerequisites

- Python 3.11 or higher
- Git installed
- GitHub account
- LeetCode account

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aptik09/leetcode-journey.git
cd leetcode-journey
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Automatic Sync Setup

### Option 1: GitHub Actions (Recommended)

The repository is already configured with GitHub Actions that will:
- Run daily at 00:00 UTC (5:30 AM IST)
- Sync your LeetCode submissions
- Update README with latest stats
- Update the atomic habits calendar

**No additional setup needed!** Just solve problems on LeetCode and the repo will auto-update.

### Option 2: Manual Sync

You can manually trigger the sync anytime:

```bash
# Sync LeetCode submissions
python scripts/sync_leetcode.py

# Update README
python scripts/update_readme.py

# Update calendar
python scripts/generate_calendar.py mark
```

### Option 3: Local Automation (Cron Job)

For Linux/Mac, add to crontab:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9 AM)
0 9 * * * cd /path/to/leetcode-journey && python scripts/sync_leetcode.py && python scripts/update_readme.py && git add . && git commit -m "Auto-sync" && git push
```

For Windows, use Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (Daily at 9 AM)
4. Action: Start a program
5. Program: `python`
6. Arguments: `scripts/sync_leetcode.py`
7. Start in: `C:\path\to\leetcode-journey`

---

## 📊 Usage

### Mark Today's Progress

```bash
# Mark that you solved 1 problem today
python scripts/generate_calendar.py mark

# Mark multiple problems
python scripts/generate_calendar.py mark 3
```

### View Statistics

```bash
# Show calendar stats
python scripts/generate_calendar.py stats

# Show current month calendar
python scripts/generate_calendar.py month

# Show full year calendar
python scripts/generate_calendar.py year
```

### Manual Sync

```bash
# Fetch latest submissions from LeetCode
python scripts/sync_leetcode.py

# Update README with new data
python scripts/update_readme.py
```

---

## 📁 Repository Structure

```
leetcode-journey/
├── .github/
│   └── workflows/
│       └── sync.yml              # GitHub Actions workflow
├── problems/                     # All solved problems
│   ├── easy/
│   │   ├── array/
│   │   ├── string/
│   │   └── ...
│   ├── medium/
│   │   ├── dynamic-programming/
│   │   ├── tree/
│   │   └── ...
│   └── hard/
│       ├── graph/
│       └── ...
├── contests/                     # Contest solutions
│   ├── weekly/
│   └── biweekly/
├── scripts/                      # Automation scripts
│   ├── sync_leetcode.py         # Sync with LeetCode
│   ├── update_readme.py         # Update README
│   └── generate_calendar.py     # Calendar management
├── stats/                        # Statistics
│   ├── progress.json            # Progress data
│   └── calendar.json            # Calendar data
├── README.md                     # Main dashboard
├── SETUP.md                      # This file
└── requirements.txt              # Python dependencies
```

---

## 🎯 How It Works

### 1. Problem Submission
When you submit a problem on LeetCode:
- The sync script fetches your recent submissions
- Extracts problem details (title, difficulty, topics)
- Creates a markdown file with problem statement
- Saves to appropriate directory (difficulty/topic)

### 2. Organization
Problems are automatically organized:
```
problems/
├── easy/
│   ├── array/
│   │   └── 1_two-sum.md
│   └── string/
│       └── 14_longest-common-prefix.md
├── medium/
│   └── dynamic-programming/
│       └── 70_climbing-stairs.md
└── hard/
    └── graph/
        └── 127_word-ladder.md
```

### 3. README Update
The README is automatically updated with:
- Total problems solved
- Current streak
- Atomic habits calendar with checkmarks
- Topic-wise problem list
- Contest performance
- Statistics and graphs

### 4. Calendar Tracking
- Each day you solve a problem gets a ✅
- Streak counter tracks consecutive days
- Monthly and yearly views available
- Statistics show total active days

---

## 🔥 Tips for Maximum Productivity

### 1. Daily Routine
- Solve at least 1 problem daily
- Run sync script after solving
- Check your streak on README
- Aim for 30-day streak!

### 2. Topic Focus
- Pick a topic (e.g., Array)
- Solve 5-10 problems in that topic
- Move to next topic
- Review periodically

### 3. Contest Participation
- Join Weekly Contest (Saturday 8 PM IST)
- Join Biweekly Contest (alternate Saturdays)
- Solutions auto-saved to contests/

### 4. Review and Revise
- Revisit old problems monthly
- Add notes to problem files
- Update complexity analysis
- Link related problems

---

## 🐛 Troubleshooting

### Sync Not Working

**Problem:** Script fails to fetch submissions

**Solution:**
1. Check internet connection
2. Verify LeetCode username in script
3. LeetCode API might be rate-limited (wait 1 hour)

### Calendar Not Updating

**Problem:** Calendar doesn't show checkmarks

**Solution:**
```bash
# Manually mark today
python scripts/generate_calendar.py mark

# Check calendar data
cat stats/calendar.json
```

### README Not Updating

**Problem:** README shows old data

**Solution:**
```bash
# Force update
python scripts/update_readme.py

# Check if stats file exists
cat stats/progress.json
```

### GitHub Actions Failing

**Problem:** Workflow fails on GitHub

**Solution:**
1. Check Actions tab on GitHub
2. View error logs
3. Ensure repository has write permissions
4. Re-run workflow manually

---

## 🎨 Customization

### Change Username

Edit `scripts/sync_leetcode.py`:
```python
LEETCODE_USERNAME = "your_username_here"
```

### Modify Calendar Style

Edit `scripts/generate_calendar.py` to change:
- Checkmark symbols (✅, 🔥, ⭐)
- Calendar layout
- Color scheme

### Add Custom Topics

Edit `scripts/sync_leetcode.py`:
```python
TOPIC_MAPPING = {
    "your-topic": "Your Topic Name",
    # Add more topics
}
```

---

## 📈 Advanced Features

### Webhook Integration

Set up a webhook to auto-sync on problem submission:

1. Create a webhook endpoint
2. Configure LeetCode to send events
3. Trigger sync script on event

### Discord/Slack Notifications

Add notifications when you:
- Solve a problem
- Break your streak record
- Complete a topic
- Participate in contest

### Analytics Dashboard

Create a web dashboard showing:
- Progress graphs
- Topic heatmap
- Difficulty distribution
- Time spent per problem

---

## 🤝 Contributing

Want to improve this tracker? Feel free to:
1. Fork the repository
2. Make improvements
3. Submit a pull request

---

## 📝 License

MIT License - Feel free to use and modify!

---

## 🙏 Acknowledgments

- LeetCode for the amazing platform
- GitHub Actions for automation
- Atomic Habits concept by James Clear

---

<div align="center">

**Happy Coding! 🚀**

Made with ❤️ by Aptik Pandey

</div>
