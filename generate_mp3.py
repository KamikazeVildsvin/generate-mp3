#!/usr/bin/env python3

import subprocess
import glob
import sys
from os import path, remove

def remove_mp3_files(path_to_folder):
    glob_str = f"{path_to_folder}/**/*.mp3"
    for name in glob.glob(glob_str, recursive=True):
        print(f"removing \"{name}\"")
        remove(name)
    print("Removed files old mp3 files...")

def convert_to_mp3(path_to_folder):
    print("Converting WAV to MP3...")
    remove_mp3_files(path_to_folder)
    glob_str = f"{path_to_folder}/**/*.wav"
    for name in glob.glob(glob_str, recursive=True):
        mp3_filename = name.replace(".wav", ".mp3")
        command = f"ffmpeg -i \"{name}\" -c:a libmp3lame -q:a 2 \"{mp3_filename}\""
        subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    print("Convertion completed...")

def convert_filename_to_title(path_to_folder):
    print("Renaming MP3 files...")
    glob_str = f"{path_to_folder}/**/*.mp3"
    for name in glob.glob(glob_str, recursive=True):
        command = f"exiftool -r '-Filename<$Title.%le' \"{name}\""
        subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    print("Renaming completed...")

def move_mp3s_to_dap_player(path_to_folder):
    print("Moving all MP3s to DAP...")
    command = f"rsync -hvr --exclude='*.wav' --include='*.mp3' \"{path_to_folder}\" \"/Volumes/Untitled\""
    subprocess.run(command, stdout=sys.stdout, stderr=sys.stderr, shell=True)
    print("Copying files completed...")

def print_help():
    help_str = """
    -- MP3 convertion tool --
    Simple CLI for automated MP3 convertion and 
    uploading to Snowsky Echo Mini DAP.

    For correct operation, ensure that the Snowsky
    Echo Mini is mounted.

    To use the script run the following command
    `python3 generate_mp3.py <path-to-folder>`
    
    # Arguments
    filepath: path to the folder that contains
    the files that are to be converted to mp3.

    ## Dependencies
    - ffmpeg
    - exiftool
    - rsync
    """
    print(help_str)

def main():
    if len(sys.argv) != 2:
        exit("Please provide the path to the folder that is to be converted!")
    input_arg = sys.argv[1]
    if input_arg == "--help" or input_arg == "-h":
        print_help()
        exit()
    path_to_folder = path.abspath(input_arg)
    if not path.isdir(path_to_folder):
        err_str = "The provided folder path doesn't exists!\n" \
        "Run `python3 generate_mp3.py -h` for help."
        exit(err_str)
    print(f"Generating MP3s recursivly from directory: {path_to_folder}")
    convert_to_mp3(path_to_folder)
    convert_filename_to_title(path_to_folder)
    move_mp3s_to_dap_player(path_to_folder)

if __name__ == "__main__":
    main()

