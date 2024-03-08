import logging
import concurrent.futures
from pathlib import Path
import time

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s"
)


class FileSearcher:
    """
    Searches for specified keywords within a file.
    This class remains unchanged as it doesn't directly handle threading or multiprocessing.
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
            return str(file_path), {}  # Return empty dict for errors
        return str(file_path), found_in_file


class ProcessManager:
    """
    Manages concurrent searches in files using ProcessPoolExecutor.
    """

    def __init__(self, keywords, file_paths, num_processes):
        if num_processes < 1:
            raise ValueError("Number of processes must be at least 1.")
        self.searcher = FileSearcher(keywords)
        self.file_paths = [Path(p) for p in file_paths]
        self.num_processes = num_processes
        self.results = {keyword: [] for keyword in keywords}

    def run_searches(self):
        """
        Executes concurrent searches across provided file paths using multiprocessing.
        """
        with concurrent.futures.ProcessPoolExecutor(
            max_workers=self.num_processes
        ) as executor:
            future_to_path = {
                executor.submit(self.searcher.search_in_file, path): path
                for path in self.file_paths
                if path.is_file()
            }
            for future in concurrent.futures.as_completed(future_to_path):
                _, found = future.result()
                for keyword, paths in found.items():
                    self.results[keyword].extend(paths)

    def get_results(self):
        """
        Returns the search results compiled from all processes.
        """
        return self.results


def main(keywords, file_paths, num_processes=4):
    try:
        start_time = time.time()
        manager = ProcessManager(keywords, file_paths, num_processes)
        manager.run_searches()
        end_time = time.time()
        logging.info(f"Execution time: {end_time - start_time:.4f} seconds")
        return manager.get_results()
    except ValueError as e:
        logging.error(f"Validation error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


# Example usage
if __name__ == "__main__":
    keywords = ["Marco", "Polo"]
    file_paths = ["./folder/subfolder_1/file_1.txt", "./folder/subfolder_2/file_2.txt"]
    num_processes = 4

    results = main(keywords, file_paths, num_processes)
    if results:
        logging.info(f"Search results: {results}")
