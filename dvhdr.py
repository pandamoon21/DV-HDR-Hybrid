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
arguments.add_argument("-o", '--output', dest="output", help="Specify output file name with no extension", required=True)
args = arguments.parse_args()

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)

dvexe = dirPath + '/dovi_tool.exe'
ffmpegexe = dirPath + '/ffmpeg.exe'
mkvmergeexe = dirPath + '/mkvmerge.exe'

output = str(args.output)

print("\nDV.HDR10 .....")
subprocess.run(f'{ffmpegexe} -i dv.mkv -an -c:v copy -f hevc dv.hevc', shell=True)
subprocess.run(f'{dvexe} extract-rpu dv.hevc', shell=True) 
subprocess.run(f'{ffmpegexe} -i hdr10.mkv -c:v copy hdr10.hevc', shell=True)  
subprocess.run(f'{dvexe} inject-rpu -i hdr10.hevc --rpu-in RPU.bin -o dvhdr.hevc', shell=True) 
subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.mkv', 'dvhdr.hevc'])

