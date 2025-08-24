import os
import hashlib
import json
import logging

# Setup basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log', mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Prevent duplicate handlers if reloaded
if not logger.hasHandlers():
    logger.addHandler(file_handler)

# Load categorization rules
def load_rules():
    try:
        with open('rules.json', 'r') as f:
            rules = json.load(f)
        logger.info("Loaded categorization rules successfully.")
        return rules
    except Exception as e:
        logger.error(f"Failed to load rules.json: {e}")
        return {}

# Generate SHA-256 hash of a file
def get_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logger.warning(f"Error hashing {filepath}: {e}")
        return None

# Categorize file based on rules
def categorize_file(filepath, rules):
    filepath_lower = filepath.lower()
    for category, keywords in rules.items():
        for keyword in keywords:
            if keyword in filepath_lower:
                logger.info(f"File {filepath} categorized under '{category}'.")
                return category
    logger.info(f"File {filepath} categorized under 'Uncategorized'.")
    return "Uncategorized"

# Scan directory and return hashed files with categories
def scan_directory(path):
    logger.info(f"Scanning directory: {path}")
    rules = load_rules()
    file_hashes = {}
    categorized_files = {}

    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            file_hash = get_file_hash(full_path)

            if not file_hash:
                continue  # skip unreadable files

            if file_hash in file_hashes:
                logger.info(f"Duplicate found: {full_path} == {file_hashes[file_hash]}")
                print(f"Duplicate found: {full_path} == {file_hashes[file_hash]}")
            else:
                file_hashes[file_hash] = full_path
                category = categorize_file(full_path, rules)
                categorized_files.setdefault(category, []).append(full_path)

    logger.info("Directory scanning completed.")
    return categorized_files

# Scan directories from config.json
def scan_directories():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        directories = config.get("scan_directories", [])
        logger.info(f"Scanning directories: {directories}")
    except Exception as e:
        logger.error(f"Failed to read config.json: {e}")
        return {}

    combined_results = {}
    for directory in directories:
        if os.path.exists(directory):
            result = scan_directory(directory)
            for category, files in result.items():
                combined_results.setdefault(category, []).extend(files)
        else:
            logger.warning(f"Directory does not exist: {directory}")

    return combined_results

def scan_for_duplicates(path):
    # Your logic here
    print("Scanning path:", path)
    return []  # Dummy return for now


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

