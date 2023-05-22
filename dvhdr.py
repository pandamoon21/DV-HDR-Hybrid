import argparse
import json
import os
import shutil
import subprocess
import sys
import pyfiglet
from rich import print
from typing import DefaultDict, Optional
from pathlib import Path

title = pyfiglet.figlet_format('Dolby Vision HDR10 Hybrid Script', font='slant')
print(f'[magenta]{title}[/magenta]')
print("by -∞WKS∞-#3982 forked by pandamoon21")
print("Required files (in PATH): dovi_tool, mkvmerge, ffmpeg\n")

arguments = argparse.ArgumentParser()
arguments.add_argument("-ih", '--input-hdr', dest="input_hdr", help="Specify input hdr file name.", required=True)
arguments.add_argument("-id", '--input-dv', dest="input_dv", help="Specify input dv file name.", required=True)
arguments.add_argument("-o", '--output', dest="output", help="Specify output file name with no extension", required=True)
arguments.add_argument("-gr", '--group', dest="group", help="Specify group name for output", required=False, default="GRP")
args = arguments.parse_args()

def get_binary_path(*names: str) -> Optional[Path]:
    """Find the path of the first found binary name."""
    for name in names:
        path = shutil.which(name)
        if path:
            return Path(path)
    return None

# binary file
dovi_tool = get_binary_path("dovi_tool")
ffmpeg = get_binary_path("ffmpeg")
mkvmerge = get_binary_path("mkvmerge")

output = str(args.output)
input_hdr = str(args.input_hdr)
input_dv = str(args.input_dv)
group = str(args.group)

print("\nExtracting video DV and generating BIN DV Profile 8.....")
subprocess.run(f'{ffmpeg} -hide_banner -loglevel warning -y -i {input_dv} -an -c:v copy -f hevc dv.hevc', shell=True)
subprocess.run(f'{dovi_tool} -m 3 extract-rpu dv.hevc', shell=True) 
print("\nAll Done .....")

print("\nExtracting video HDR.....")
subprocess.run(f'{ffmpeg} -hide_banner -loglevel warning -y -i {input_hdr} -c:v copy hdr10.hevc', shell=True)  
print("\nAll Done .....") 

print("\nMerger DV Profile 8 and HDR.....")
subprocess.run(f'{dovi_tool} inject-rpu -i hdr10.hevc --rpu-in RPU.bin -o dvhdr.hevc', shell=True) 
print("\nAll Done .....")

print("\nMux.....")
subprocess.run([str(mkvmerge), '--ui-language' ,'en', '--output', f'{output}.DV.HDR.H.265-{group}.mkv', 'dvhdr.hevc', '--no-video', {input_hdr}])
print("\nAll Done .....")    

print("\nDeleting unused files...")
Path("dv.hevc").unlink()
Path("hdr10.hevc").unlink()
Path("RPU.bin").unlink()
Path("dvhdr.hevc").unlink()

