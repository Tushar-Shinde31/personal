import argparse
import random
import subprocess
from datetime import datetime, timedelta

def parse_arguments():
    parser = argparse.ArgumentParser(description="Control Git commit contributions.")
    parser.add_argument("--max_commits", type=int, default=10, help="Maximum commits per day.")
    parser.add_argument("--no_weekends", action="store_true", help="Skip weekends.")
    parser.add_argument("--days_before", type=int, default=365, help="Days before today to start contributions.")
    parser.add_argument("--days_after", type=int, default=0, help="Days after today to end contributions.")
    parser.add_argument("--frequency", type=float, default=0.5, help="Probability of contributing on a day (0-1).")
    return parser.parse_args()

def generate_commits(date, max_commits):
    """Generate a random number of commits for a specific day."""
    num_commits = random.randint(1, max_commits)
    for _ in range(num_commits):
        message = f"Commit on {date}"
        subprocess.run(['git', 'commit', '--allow-empty', '-m', message, '--date', date])

def main():
    args = parse_arguments()

    # Define start and end dates
    today = datetime.now()
    start_date = today - timedelta(days=args.days_before)
    end_date = today + timedelta(days=args.days_after)

    current_date = start_date

    # Loop through the date range
    while current_date <= end_date:
        if args.no_weekends and current_date.weekday() >= 5:
            # Skip weekends if --no_weekends is set
            current_date += timedelta(days=1)
            continue

        if random.random() < args.frequency:
            # Generate commits only with a certain frequency
            date_str = current_date.strftime("%Y-%m-%d %H:%M:%S")
            generate_commits(date_str, args.max_commits)
            print(f"Generated commits for {date_str}")

        current_date += timedelta(days=1)

    # Push changes to the repository
    subprocess.run(['git', 'push', 'origin', 'main'])
    print("Contributions pushed to GitHub.")

if __name__ == "__main__":
    main()
