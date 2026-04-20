import csv
import os
from datetime import date

FILE = "attendance.csv"

def mark_attendance(name):
    today = str(date.today())
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, today, "Present"])
    print(f"  ✓ {name} marked as Present on {today}")

def mark_absent(name):
    today = str(date.today())
    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, today, "Absent"])
    print(f"  ✗ {name} marked as Absent on {today}")

def view_attendance():
    if not os.path.exists(FILE):
        print("  No records found yet.")
        return
    print(f"\n  {'Name':<20} {'Date':<15} {'Status'}")
    print("  " + "-" * 45)
    with open(FILE, "r") as f:
        for row in csv.reader(f):
            if row:
                print(f"  {row[0]:<20} {row[1]:<15} {row[2]}")

def view_by_name(name):
    if not os.path.exists(FILE):
        print("  No records found yet.")
        return
    found = False
    print(f"\n  Records for: {name}")
    print("  " + "-" * 35)
    with open(FILE, "r") as f:
        for row in csv.reader(f):
            if row and row[0].lower() == name.lower():
                print(f"  {row[1]}  ->  {row[2]}")
                found = True
    if not found:
        print("  No records found for this name.")

def summary():
    if not os.path.exists(FILE):
        print("  No records found yet.")
        return
    counts = {}
    with open(FILE, "r") as f:
        for row in csv.reader(f):
            if row:
                n = row[0]
                s = row[2]
                if n not in counts:
                    counts[n] = {"Present": 0, "Absent": 0}
                counts[n][s] = counts[n].get(s, 0) + 1
    print(f"\n  {'Name':<20} {'Present':<10} {'Absent'}")
    print("  " + "-" * 40)
    for name, data in counts.items():
        print(f"  {name:<20} {data.get('Present',0):<10} {data.get('Absent',0)}")

def main():
    print("\n" + "=" * 40)
    print("      ATTENDANCE TRACKER")
    print("=" * 40)

    while True:
        print("""
  1. Mark Present
  2. Mark Absent
  3. View All Attendance
  4. Search by Name
  5. Summary
  6. Exit
""")
        choice = input("  Enter choice (1-6): ").strip()

        if choice == "1":
            name = input("  Enter name: ").strip()
            mark_attendance(name)
        elif choice == "2":
            name = input("  Enter name: ").strip()
            mark_absent(name)
        elif choice == "3":
            view_attendance()
        elif choice == "4":
            name = input("  Enter name to search: ").strip()
            view_by_name(name)
        elif choice == "5":
            summary()
        elif choice == "6":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Try again.")

if __name__ == "__main__":
    main()
