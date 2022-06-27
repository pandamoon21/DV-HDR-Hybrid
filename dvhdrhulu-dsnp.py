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

hdrplusexe = dirPath + '/hdr10plus_tool.exe'
dvexe = dirPath + '/dovi_tool.exe'
ffmpegexe = dirPath + '/ffmpeg.exe'
mkvmergeexe = dirPath + '/mkvmerge.exe'

output = str(args.output)

print("\nDV.HDR .....") 
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i hulu.mkv -c:v copy hulu.hevc', shell=True)  
subprocess.run(f'{hdrplusexe} extract hulu.hevc -o hulu.json', shell=True) 
subprocess.run(f'{dvexe} extract-rpu hulu.hevc', shell=True) 
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i dsnp.mkv -c:v copy dsnp.hevc', shell=True)
subprocess.run(f'{hdrplusexe} inject -i dsnp.hevc -j hulu.json -o dsnphdr10plus.hevc', shell=True) 
subprocess.run(f'{dvexe} inject-rpu -i dsnphdr10plus.hevc --rpu-in RPU.bin -o dvhdr10plus.hevc', shell=True)
subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.DV.HDR.H.265-GRP.mkv', 'dvhdr10plus.hevc', '--no-video', '--no-global-tags', '--title', output +'.DV.HDR.H.265-WKS', 'dsnp.mkv'])
print("\nAll Done .....")    


print("\nDo you want to delete the Extra Files : Press 1 for yes , 2 for no")
delete_choice = int(input("Enter Response : "))

if delete_choice == 1:
    os.remove("hulu.hevc")
    os.remove("RPU.bin")
    os.remove("dsnphdr10plus.hevc")
    os.remove("dvhdr10plus.hevc")
    os.remove("hulu.json")
    os.remove("dsnp.hevc")
    try:    
        os.remove("en.srt")
    except:
        pass
else:
    pass

