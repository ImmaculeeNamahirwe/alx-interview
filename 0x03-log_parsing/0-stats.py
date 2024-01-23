#!/usr/bin/python3
import sys

def print_stats(total_size, status_codes):
    """Print statistics based on the accumulated data."""
    print("File size: {}".format(total_size))
    for code in sorted(status_codes.keys()):
        print("{}: {}".format(code, status_codes[code]))

def parse_line(line, total_size, status_codes):
    """Parse a line and update the total size and status codes counts."""
    try:
        parts = line.split()
        if len(parts) >= 9:
            size = int(parts[-1])
            status_code = int(parts[-2])
            total_size += size
            if status_code in [200, 301, 400, 401, 403, 404, 405, 500]:
                status_codes[status_code] = status_codes.get(status_code, 0) + 1
        return total_size, status_codes
    except (ValueError, IndexError):
        # Ignore lines that do not match the expected format
        return total_size, status_codes

def main():
    total_size = 0
    status_codes = {}
    lines_processed = 0

    try:
        for line in sys.stdin:
            total_size, status_codes = parse_line(line.strip(), total_size, status_codes)
            lines_processed += 1

            if lines_processed % 10 == 0:
                print_stats(total_size, status_codes)

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (CTRL + C) and print the final statistics
        print_stats(total_size, status_codes)
        sys.exit(0)

if __name__ == "__main__":
    main()
