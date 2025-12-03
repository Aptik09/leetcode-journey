# ⚡ Quick Start Guide

Get your LeetCode Journey tracker up and running in 5 minutes!

---

## 🚀 Step 1: Clone the Repository

```bash
git clone https://github.com/Aptik09/leetcode-journey.git
cd leetcode-journey
```

---

## 📦 Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! Only 2 dependencies needed.

---

## 🎯 Step 3: First Sync

Run your first sync to fetch your LeetCode data:

```bash
python scripts/sync_leetcode.py
```

This will:
- ✅ Fetch your recent submissions from LeetCode
- ✅ Create problem files organized by difficulty and topic
- ✅ Update your statistics

---

## 📊 Step 4: Update Your Dashboard

Generate your beautiful README dashboard:

```bash
python scripts/update_readme.py
```

This creates:
- ✅ Atomic habits calendar with checkmarks
- ✅ Problem statistics
- ✅ Topic-wise problem lists
- ✅ Streak counter

---

## ✅ Step 5: Mark Today

Mark that you solved problems today:

```bash
# Mark 1 problem
python scripts/generate_calendar.py mark

# Mark multiple problems
python scripts/generate_calendar.py mark 3
```

---

## 🔄 Daily Workflow

### After Solving a Problem on LeetCode:

```bash
# 1. Sync your submissions
python scripts/sync_leetcode.py

# 2. Update README
python scripts/update_readme.py

# 3. Mark calendar
python scripts/generate_calendar.py mark

# 4. Commit and push
git add .
git commit -m "✅ Solved: [Problem Name]"
git push
```

### Or Use This One-Liner:

```bash
python scripts/sync_leetcode.py && python scripts/update_readme.py && python scripts/generate_calendar.py mark && git add . && git commit -m "🚀 Daily sync" && git push
```

---

## 🤖 Automatic Sync (Recommended)

The repository already has GitHub Actions configured!

**It will automatically:**
- Run daily at 5:30 AM IST
- Sync your LeetCode submissions
- Update README and calendar
- Commit and push changes

**No manual work needed!** Just solve problems on LeetCode and your repo updates automatically.

---

## 📱 View Your Progress

### On GitHub
Visit: https://github.com/Aptik09/leetcode-journey

You'll see:
- 🔥 Current streak
- 📊 Problems solved
- 📅 Atomic habits calendar
- 📚 Topic-wise problems
- 🏆 Contest performance

### Locally

```bash
# View calendar
python scripts/generate_calendar.py month

# View statistics
python scripts/generate_calendar.py stats

# View full year
python scripts/generate_calendar.py year
```

---

## 🎯 Pro Tips

### 1. Daily Habit
- Solve at least 1 problem daily
- Maintain your streak! 🔥
- Aim for 30-day streak

### 2. Topic Focus
- Master one topic at a time
- Solve 10 problems per topic
- Review weekly

### 3. Contest Participation
- Join Weekly Contest (Saturday 8 PM IST)
- Join Biweekly Contest (alternate Saturdays)
- Solutions auto-saved!

### 4. Track Progress
- Check README daily
- Celebrate milestones
- Share your progress!

---

## 🐛 Troubleshooting

### Sync Not Working?

```bash
# Check your internet connection
ping leetcode.com

# Try manual sync
python scripts/sync_leetcode.py
```

### Calendar Not Updating?

```bash
# Manually mark today
python scripts/generate_calendar.py mark

# Check calendar data
cat stats/calendar.json
```

### Need Help?

Check the detailed [SETUP.md](SETUP.md) guide.

---

## 🎉 You're All Set!

Now go solve some problems on LeetCode and watch your repository automatically track your progress!

**Your journey to LeetCode mastery starts now!** 🚀

---

## 📈 Next Steps

1. ✅ Solve your first problem today
2. ✅ Run the sync script
3. ✅ Check your updated README
4. ✅ Share your progress!

---

<div align="center">

**Happy Coding!** 💻

Made with ❤️ by Aptik Pandey

</div>
