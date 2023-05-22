import os
import json
import subprocess
import argparse
import sys
import pyfiglet
from rich import print
from typing import DefaultDict

title = pyfiglet.figlet_format('Dolby Vision HDR10 Hybrid Script', font='slant')
print(f'[magenta]{title}[/magenta]')
print("by -∞WKS∞-#3982")
print("Required files : dovi_tool.exe, mkvmerge.exe, ffmpeg.exe\n")

arguments = argparse.ArgumentParser()
arguments.add_argument("-ih", '--input-hdr', dest="input_hdr", help="Specify input hdr file name.", required=True)
arguments.add_argument("-id", '--input-dv', dest="input_dv", help="Specify input dv file name.", required=True)
arguments.add_argument("-o", '--output', dest="output", help="Specify output file name with no extension", required=True)
arguments.add_argument("-gr", '--group', dest="group", help="Specify group name for output", required=False, default="GRP")
args = arguments.parse_args()

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

dvexe = dirPath + '/dovi_tool.exe'
ffmpegexe = dirPath + '/ffmpeg.exe'
mkvmergeexe = dirPath + '/mkvmerge.exe'

output = str(args.output)
input_hdr = str(args.input_hdr)
input_dv = str(args.input_dv)
group = str(args.group)

print("\nExtracting video DV and generating BIN DV Profile 8.....")
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i {input_dv} -an -c:v copy -f hevc dv.hevc', shell=True)
subprocess.run(f'{dvexe} -m 3 extract-rpu dv.hevc', shell=True) 
print("\nAll Done .....")
print("\nExtracting video HDR.....")
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i {input_hdr} -c:v copy hdr10.hevc', shell=True)  
print("\nAll Done .....") 
print("\nMerger DV Profile 8 and HDR.....")
subprocess.run(f'{dvexe} inject-rpu -i hdr10.hevc --rpu-in RPU.bin -o dvhdr.hevc', shell=True) 
print("\nAll Done .....")
print("\nMux.....")
subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output + f'.DV.HDR.H.265-{group}.mkv', 'dvhdr.hevc', '--no-video', 'hdr10.mkv'])
print("\nAll Done .....")    
print("\nDeleting unused files...")
os.remove("dv.hevc")
os.remove("hdr10.hevc")
os.remove("RPU.bin")
os.remove("dvhdr.hevc")

