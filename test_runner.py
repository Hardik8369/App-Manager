from scanner.utils import scan_directories

categorized = scan_directories()

for category, files in categorized.items():
    print(f"\nCategory: {category}")
    for file in files:
        print(f" - {file}")
