import os
import json
import subprocess
import argparse
import sys
import pyfiglet
from rich import print
from typing import DefaultDict

title = pyfiglet.figlet_format('Dolby Vision HDR10Plus Hybrid Script', font='slant')
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

print("\nExtracting video HDR and generating BIN DV Profile 8.....")
subprocess.run(f'{ffmpegexe} -hide_banner -loglevel warning -y -i hdr10plus.mkv -c:v copy hdr10plus.hevc', shell=True)  
subprocess.run(f'{hdrplusexe} extract hdr10plus.hevc -o hdr10plus_manifest.json', shell=True) 
subprocess.run(f'{dvexe} generate -j default_cmv40.json --hdr10plus-json hdr10plus_manifest.json -o dvhdr10plus.bin', shell=True) 
print("\nAll Done .....")
print("\nMerger DV Profile 8 and HDR.....")
subprocess.run(f'{dvexe} inject-rpu -i hdr10plus.hevc --rpu-in dvhdr10plus.bin -o dvhdr10plus.hevc', shell=True)
print("\nAll Done .....")
print("\nMux.....")
subprocess.run([mkvmergeexe, '--ui-language' ,'en', '--output', output +'.DV.HDR.H.265-GRP.mkv', 'dvhdr10plus.hevc', '--no-video', 'hdr10plus.mkv'])
print("\nAll Done .....")    


print("\nDo you want to delete the Extra Files : Press 1 for yes , 2 for no")
delete_choice = int(input("Enter Response : "))

if delete_choice == 1:
    os.remove("hdr10plus.hevc")
    os.remove("dvhdr10plus.bin")
    os.remove("dvhdr10plus.hevc")
    os.remove("hdr10plus_manifest.json")
    try:    
        os.remove("en.srt")
    except:
        pass
else:
    pass

