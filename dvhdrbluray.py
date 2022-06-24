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

print("\nDV.HDR .....")
subprocess.run(f'{mkvmergeexe} -o audiosubs.mka  --no-video hdrbluray.mkv', shell=True) 
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i hdrbluray.mkv -c:v copy hdrbluray.hevc', shell=True)  
subprocess.run(f'{dvexe} -m 3 extract-rpu hdrbluray.hevc', shell=True) 
subprocess.run(f'{dvexe} inject-rpu -i hdrbluray.hevc --rpu-in RPU.bin -o dvhdrbluray.hevc', shell=True) 
subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.DV.HDR.H.265-GRP.mkv', 'dvhdrbluray.hevc', 'audiosubs.mka'])
print("\nAll Done .....")    


print("\nDo you want to delete the Extra Files : Press 1 for yes , 2 for no")
delete_choice = int(input("Enter Response : "))

if delete_choice == 1:
    os.remove("hdrbluray.mkv")
    os.remove("RPU.bin")
    os.remove("dvhdrbluray.hevc")
    os.remove("audiosubs.mka")
    try:    
        os.remove("en.srt")
    except:
        pass
else:
    pass

