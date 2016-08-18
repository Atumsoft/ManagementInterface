import subprocess
import re


INTERFACE_NUMBER_EXPR = re.compile(r'[0-9]+')
TAPDEV_NUMBER_EXPR = re.compile(r'TAP-Windows Adapter.*')

def spliceRouteTable():
    proc = subprocess.Popen('route print', stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    tapDevNumDict = {} # k: tap device number, v: interface number in routing table
    for line in output.split('\n'):
        if line.startswith('='): continue
        if 'TAP-Windows Adapter' in line:
            match = re.search(INTERFACE_NUMBER_EXPR, line).group(0)
            ifNum = int(match)
            match = re.search(TAPDEV_NUMBER_EXPR, line).group(0)

            if match.strip().endswith('V9'): # have to make an exception for first adapter with no #
                tapDevNum = 1
            else:
                tapDevNum = int(match.strip()[-1])

            tapDevNumDict[tapDevNum] = ifNum
    return tapDevNumDict

if __name__ == '__main__':
   print spliceRouteTable()