import argparse
from pathlib import Path
from attack_info.getAttackInfo import *

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="Path directory of enumeration files")
ap.add_argument("-n", "--name", required=False, help="Name of output file")
ap.add_argument("-o", "--output", required=False, help="Output folder path")
args = vars(ap.parse_args())

path = Path(args['path'])
name = args['name'] or 'output.md'
output = Path(args['output']) or Path.cwd()

create_attack_info(path, name, output)
