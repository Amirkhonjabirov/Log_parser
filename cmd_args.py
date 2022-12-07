import sys
import os

log_files = []
dir_for_parsed_files = ''

if len(sys.argv) == 1:
    print("Path to the directory or to the log file is required as the first argument")
else:
    if sys.argv[1].endswith(".log") and os.path.isfile(sys.argv[1]):
        log_files.append(sys.argv[1])
    elif os.path.isdir(sys.argv[1]):
        os.chdir(sys.argv[1])
        dir_path = sys.argv[1]
        if not dir_path.endswith('/'):
            dir_path += '/'
        log_files.extend([dir_path + i for i in os.listdir() if i.endswith(".log")])
        if len(log_files) == 0:
            print(f"No log files in this directory: {dir_path}")
            sys.exit(0)
    else:
        print("Wrong first argument, not a log file or directory")

    if len(sys.argv) == 3:
        if os.path.isdir(sys.argv[2]):
            dir_for_parsed_files = sys.argv[2]
            if not dir_for_parsed_files.endswith('/'):
                dir_for_parsed_files += '/'
            print(f"Parsed log file(s) will be saved to the {dir_for_parsed_files} folder\n")
    else:
        print("Parsed log file(s) will be saved to the current directory\n")