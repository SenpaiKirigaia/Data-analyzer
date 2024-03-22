import argparse
import logging
import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from get_data import get_data


class FileChangeHandler(FileSystemEventHandler):
    """
    A class that handles file changes.
    """

    def __init__(self, folder):
        self.directory = os.path.abspath(folder)
        self.file_indices = {}
        self.data = None
        self.index = 1

    def on_modified(self, event):
        """
        Called when a file or a directory is modified.

        :param event:
        :return: None
        """
        if not event.is_directory:
            abs_path = os.path.abspath(event.src_path)
            if os.path.dirname(abs_path) == self.directory:
                logging.info("File {} has been modified. Processing...".format(abs_path))
                try:
                    # Process the file and get the updated index
                    self.data, index = get_data(abs_path, data=self.data, index=self.file_indices.get(abs_path, 1))
                    self.file_indices[abs_path] = index
                    logging.info(f"Index for {abs_path}: {index}")

                    # Find the file with the highest index
                    max_index_file = max(self.file_indices, key=self.file_indices.get)
                    # self.index = max(self.file_indices.items())
                    # self.file_indices = {max_index_file: self.index}
                    # Delete other files
                    for f in os.listdir(self.directory):
                        file_path = os.path.join(self.directory, f)
                        if os.path.isfile(file_path) and file_path != max_index_file:
                            os.remove(file_path)
                except Exception as error:
                    logging.error("Failed to process file: {}".format(error))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log files in a directory and output their data to a JSON "
                                                 "file.")
    parser.add_argument("dirpath", help="Path to the directory containing log files.")
    args = parser.parse_args()

    directory = args.dirpath

    if not os.path.isdir(directory):
        logging.error("The path {} is not a directory.".format(directory))
        exit(1)

    # Create an event handler and an observer
    event_handler = FileChangeHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, path=directory, recursive=False)
    observer.start()

    # Start the observer and wait for keyboard interrupt
    try:
        while True:
            time.sleep(0.0001)  # Needed for the observer to not eat up the CPU. Change the value as you see fit.
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
        observer.stop()
    finally:
        observer.join()

    # Instructions for running:
    # Run the script from the command line, specifying the path to the directory containing log files:
    # python log-analyser.py /path/to/your/directory
