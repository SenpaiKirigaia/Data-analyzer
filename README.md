# Data-analyzer

## Overview
Data-analyzer is a Python project designed for scraping log files in the directory and analyzing data from various devices. It processes log files to extract information and sends this data to a designated API endpoint.

## Repository Structure
The repository consists of three main Python files:
- `log_analyzer.py`: This is the main script that sets up a file watcher to monitor changes in a directory. Upon detecting a modification, it processes the file to extract data, then deletes files with fewer measurements.
- `get_data.py`: Contains the logic for extracting data from the monitored log file. It supports multiple device types and formats the data for further processing.
- `send_data.py`: Handles sending the processed data to a defined API endpoint. It ensures that each piece of data is sent only once, avoiding duplicates.

## Features
- **Real-time File Monitoring**: Uses Watchdog library to monitor changes in log files in real-time.
- **Multi-Device Support**: Capable of extracting data from different types of devices, thanks to flexible data extraction methods.
- **Duplicate Avoidance**: Implements logic to prevent resending of data, enhancing data integrity.

## Installation
1. Clone the repository:

    ```sh
    git clone https://github.com/SenpaiKirigaia/Data-analyzer.git
2. Install the required packages:
   
    ```sh
    pip install -r requirements.txt
    ```
3. Create auth.py file and write the API endpoint and authorization details in it. The file should look like this:

```python
# auth.py
headers = {
    'Authorization': 'token',
    'content-type': "application/json"
}

url = 'https://api.example.com' 
```

## Alternative installation
1. Clone directory to "C:\Users\your_name\mitra\log-analyzer".
2. Run install.bat
3. Change directory for monitoring in the log.bat and run it
## Usage
1. Modify the `log_analyzer.py` file to specify the path of the directory with log files you wish to monitor.
2. Run `log_analyzer.py`:
    
    ```sh
    python log_analyzer.py /path/to/your/directory
    ```
3. The script will start monitoring the log file for any changes and process new data as it comes in.

## Configuration
- Write the API endpoint and authorization details in `auth.py` to match your specific requirements.
- Adjust the file path in `log_analyzer.py` to point to your log file.
- Modify the `get_data.py` file to support additional device types.
