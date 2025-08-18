#!/usr/bin/env python3
"""
Script to split raw data file into smaller files by month.
Only takes tickets with Release date within the timeframe from now to 2 months in the future.
"""

import re
import os
from collections import defaultdict
from datetime import datetime, timedelta

def extract_updated_time(line):
    """Extract updated time from a line."""
    # Pattern to match: Updated Time: 2025-07-21T10:17:33.050+0900
    pattern = r'Updated Time:\s*(\d{4}-\d{2}-\d{2})T'
    match = re.search(pattern, line)
    
    if match:
        return match.group(1)
    return None

def extract_release_dates(line):
    """Extract all release dates from a line."""
    dates = []
    # Pattern to match dates like 2025-05-27, 2025-08-26,2025-07-08
    date_pattern = r'Release date:\s*([0-9-,\s]+)'
    match = re.search(date_pattern, line)
    
    if match:
        date_str = match.group(1).strip()
        # Split by comma if multiple dates
        for date in date_str.split(','):
            date = date.strip()
            if re.match(r'\d{4}-\d{2}-\d{2}', date):
                dates.append(date)
    
    return dates

def is_within_date_range(date_str, start_date, end_date):
    """Check if a date string is within the specified range."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return start_date <= date_obj <= end_date
    except:
        return False

def should_include_ticket(line, future_cutoff_date):
    """Check if ticket should be included based on release dates only."""
    # Check release dates (from now to 2 months in the future)
    release_dates = extract_release_dates(line)
    if not release_dates:
        return False
    
    # At least one release date must be within the next 2 months from now
    now = datetime.now()
    for date_str in release_dates:
        if is_within_date_range(date_str, now, future_cutoff_date):
            return True
    
    return False

def get_month_year(date_str):
    """Get month and year from date string."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.year, date_obj.month
    except:
        return None, None

def get_month_number(month):
    """Get month number as padded string."""
    return f"{month:02d}"

def main():
    input_file = "data/raw/release-announcement.md"
    output_dir = "data/processed"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate date range for release date filtering
    now = datetime.now()
    # Next 2 months for release date filtering
    future_cutoff_date = now + timedelta(days=60)  # Approximately 2 months
    
    print("🔍 Analyzing raw data file...")
    print(f"📅 Filtering criteria:")
    print(f"   - Release Date: from {now.strftime('%Y-%m-%d')} to {future_cutoff_date.strftime('%Y-%m-%d')}")
    
    # Dictionary to store lines by month pairs
    month_data = defaultdict(list)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    total_lines = 0
    filtered_lines = 0
    
    # Process each line
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
            
        total_lines += 1
        
        # Check if ticket should be included based on release date filtering
        if not should_include_ticket(line, future_cutoff_date):
            continue
        
        filtered_lines += 1
        
        # Extract release dates from this line
        release_dates = extract_release_dates(line)
        
        if release_dates:
            # For each release date, determine which month files it belongs to
            for date_str in release_dates:
                year, month = get_month_year(date_str)
                if year and month:
                    # Add to current month file (contains current + next month)
                    current_key = f"{year}-{month:02d}"
                    month_data[current_key].append(line)
                    
                    # Add to previous month file (contains previous + current month)
                    if month > 1:
                        prev_key = f"{year}-{(month-1):02d}"
                        month_data[prev_key].append(line)
                    else:
                        # Handle January case (previous month is December of previous year)
                        prev_key = f"{year-1}-12"
                        month_data[prev_key].append(line)
    
    print(f"📊 Filtered {filtered_lines} tickets out of {total_lines} total lines")
    
    # Remove duplicate lines in each month file
    for key in month_data:
        month_data[key] = list(set(month_data[key]))
    
    print(f"📊 Found data for {len(month_data)} month groups (after filtering)")
    
    # Write files for each month
    for month_key in sorted(month_data.keys()):
        year, month = month_key.split('-')
        year, month = int(year), int(month)
        
        # Calculate next month for filename
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        # Create filename
        current_month_num = get_month_number(month)
        next_month_num = get_month_number(next_month)
        filename = f"release-data-{year}-{current_month_num}-and-{next_year}-{next_month_num}.md"
        filepath = os.path.join(output_dir, filename)
        
        # Write file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Release Data - Month {month}/{year} and Month {next_month}/{next_year}\n")
            f.write(f"# Filtered data: Release Date from now to 2 months in the future\n")
            f.write(f"# Total: {len(month_data[month_key])} tickets\n\n")
            
            for line in sorted(month_data[month_key]):
                f.write(line + '\n')
        
        print(f"✅ Created file: {filename} ({len(month_data[month_key])} tickets)")
    
    print(f"\n🎉 Completed! Created {len(month_data)} files in {output_dir}/")
    
    # Show summary
    print("\n📋 Summary (Filtered Data):")
    total_tickets = 0
    for month_key in sorted(month_data.keys()):
        year, month = month_key.split('-')
        count = len(month_data[month_key])
        total_tickets += count
        print(f"   - Month {month}/{year}: {count} tickets")
    
    print(f"\nTotal filtered tickets processed: {total_tickets}")
    print(f"Original total lines: {total_lines} -> Filtered to: {filtered_lines} tickets")

if __name__ == "__main__":
    main() 