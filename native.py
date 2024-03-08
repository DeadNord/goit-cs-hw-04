import logging
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class FileSearcher:
    """
    Searches for specified keywords within a file.
    """
    def __init__(self, keywords):
        if not keywords:
            raise ValueError("Keywords list cannot be empty.")
        self.keywords = keywords

    def search_in_file(self, file_path):
        """
        Searches for the keywords in a single file and returns found entries.
        """
        found_in_file = {keyword: [] for keyword in self.keywords}
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                for keyword in self.keywords:
                    if keyword in content:
                        found_in_file[keyword].append(str(file_path))
        except IOError as e:
            logging.error(f"Error opening or reading file {file_path}: {e}")
            return {}  # Return empty dict for errors
        return found_in_file

def main(keywords, file_paths):
    try:
        start_time = time.time()
        searcher = FileSearcher(keywords)
        results = {keyword: [] for keyword in keywords}

        for file_path in file_paths:
            path = Path(file_path)
            if path.is_file():
                found = searcher.search_in_file(path)
                for keyword, paths in found.items():
                    results[keyword].extend(paths)

        end_time = time.time()
        logging.info(f"Execution time: {end_time - start_time:.4f} seconds")
        return results
    except ValueError as e:
        logging.error(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Example usage
if __name__ == "__main__":
    keywords = ["Marco", "Polo"]
    file_paths = ["./folder/subfolder_1/file_1.txt", "./folder/subfolder_2/file_2.txt"]

    results = main(keywords, file_paths)
    if results:
        logging.info(f"Search results: {results}")
