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

    def __init__(self, filename):
        self.filename = os.path.abspath(filename)

    def on_modified(self, event):
        """
        Called when a file or a directory is modified.

        :param event:
        :return: None
        """
        if not event.is_directory:
            abs_path = os.path.abspath(event.src_path)
            if abs_path == self.filename:
                logging.info("File {} has been modified. Updating output.json...".format(self.filename))
            try:
                # Process the file
                get_data(self.filename)
            except Exception as e:
                logging.error("Failed to process file: {}".format(e))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a log file and output its data to a JSON file.")
    parser.add_argument("filepath", help="Path to the log file to be processed.")
    args = parser.parse_args()

    path = args.filepath

    # uncomment for manual testing
    # path = "log.txt"

    if not os.path.exists(path):
        logging.error("The file {} does not exist.".format(path))
        exit(1)

    # Create an event handler and an observer
    event_handler = FileChangeHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(path), recursive=False)
    observer.start()

    # Start the observer and wait for keyboard interrupt
    try:
        while True:
            time.sleep(0.001)  # needed for the observer to not eat up the CPU. Change the value as you see fit.
    except KeyboardInterrupt:
        observer.stop()
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
        observer.stop()
    finally:
        observer.join()

    # Инструкции по запуску:
    # Запустите скрипт из командной строки, указав путь к файлу, который нужно отслеживать:
    # python log-analyser.py /path/to/your/file.txt

    # Instructions for running:
    # Run the script from the command line, specifying the path to the file to be tracked:
    # python log-analyser.py /path/to/your/file.txt
