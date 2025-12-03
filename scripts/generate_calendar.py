#!/usr/bin/env python3
"""
Calendar Generation Script
Generates atomic habits style calendar with checkmarks
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
import calendar

BASE_DIR = Path(__file__).parent.parent
STATS_DIR = BASE_DIR / "stats"


class CalendarGenerator:
    def __init__(self):
        self.calendar_file = STATS_DIR / "calendar.json"
        self.calendar_data = self.load_calendar()
    
    def load_calendar(self):
        """Load existing calendar data"""
        if self.calendar_file.exists():
            with open(self.calendar_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_calendar(self):
        """Save calendar data"""
        with open(self.calendar_file, 'w') as f:
            json.dump(self.calendar_data, f, indent=2)
    
    def mark_today(self, problems_count=1):
        """Mark today as completed"""
        today = datetime.now().date().isoformat()
        
        if today in self.calendar_data:
            self.calendar_data[today]['count'] += problems_count
        else:
            self.calendar_data[today] = {
                'count': problems_count,
                'timestamp': datetime.now().isoformat()
            }
        
        self.save_calendar()
        print(f"✅ Marked {today} with {problems_count} problem(s)")
    
    def generate_month_calendar(self, year, month):
        """Generate calendar for specific month"""
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        
        # ASCII calendar
        calendar_str = f"\n{month_name} {year}\n"
        calendar_str += "=" * 30 + "\n"
        calendar_str += "Sun Mon Tue Wed Thu Fri Sat\n"
        
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
        
        return calendar_str
    
    def generate_year_calendar(self, year):
        """Generate full year calendar"""
        year_cal = f"\n{'='*50}\n"
        year_cal += f"  LeetCode Journey - {year}\n"
        year_cal += f"{'='*50}\n\n"
        
        for month in range(1, 13):
            year_cal += self.generate_month_calendar(year, month)
            year_cal += "\n"
        
        return year_cal
    
    def get_streak(self):
        """Calculate current streak"""
        if not self.calendar_data:
            return 0
        
        dates = sorted(self.calendar_data.keys(), reverse=True)
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
    
    def get_stats(self):
        """Get calendar statistics"""
        total_days = len(self.calendar_data)
        total_problems = sum(day['count'] for day in self.calendar_data.values())
        streak = self.get_streak()
        
        # Find longest streak
        longest_streak = 0
        current_streak = 0
        dates = sorted(self.calendar_data.keys())
        
        for i, date_str in enumerate(dates):
            if i == 0:
                current_streak = 1
            else:
                prev_date = datetime.fromisoformat(dates[i-1]).date()
                curr_date = datetime.fromisoformat(date_str).date()
                
                if (curr_date - prev_date).days == 1:
                    current_streak += 1
                else:
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1
        
        longest_streak = max(longest_streak, current_streak)
        
        return {
            'total_days': total_days,
            'total_problems': total_problems,
            'current_streak': streak,
            'longest_streak': longest_streak,
            'average_per_day': total_problems / total_days if total_days > 0 else 0
        }
    
    def display_stats(self):
        """Display calendar statistics"""
        stats = self.get_stats()
        
        print("\n" + "="*50)
        print("  📊 LEETCODE CALENDAR STATISTICS")
        print("="*50)
        print(f"  Total Active Days: {stats['total_days']}")
        print(f"  Total Problems: {stats['total_problems']}")
        print(f"  Current Streak: 🔥 {stats['current_streak']} days")
        print(f"  Longest Streak: 🏆 {stats['longest_streak']} days")
        print(f"  Average/Day: {stats['average_per_day']:.1f} problems")
        print("="*50 + "\n")


def main():
    """Main entry point"""
    import sys
    
    generator = CalendarGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "mark":
            # Mark today
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 1
            generator.mark_today(count)
        
        elif command == "stats":
            # Show statistics
            generator.display_stats()
        
        elif command == "month":
            # Show current month
            now = datetime.now()
            print(generator.generate_month_calendar(now.year, now.month))
        
        elif command == "year":
            # Show full year
            year = int(sys.argv[2]) if len(sys.argv) > 2 else datetime.now().year
            print(generator.generate_year_calendar(year))
        
        else:
            print("Unknown command. Use: mark, stats, month, or year")
    
    else:
        # Default: show current month and stats
        now = datetime.now()
        print(generator.generate_month_calendar(now.year, now.month))
        generator.display_stats()


if __name__ == "__main__":
    main()
