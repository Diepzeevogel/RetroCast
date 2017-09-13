import sys
import os
import psutil
import subprocess
import time
import re

#############################################################################################
#                                      RetroCast script                                     #
#                                                                                           #
# Version 0.1 by Diepzeevogel                                                               #
#                                                                                           #
# Based on daftmike's Mini NES Cartridge script                                             #
# https://github.com/imdaftmike/NESPi                                                       #
#                                                                                           #
#############################################################################################

#############################################################################################
# Checks if given arguments are valid
def valid_game(console, game):
    emulators = ["amiga", "amstradcpc", "apple2", "arcade", "atari800", "atari2600", "atari5200", "atari7800",
                 "atarilynx", "atarist", "c64", "coco", "dragon32", "dreamcast", "fba", "fds", "gamegear", "gb", "gba",
                 "gbc", "intellivision", "macintosh", "mame-advmame", "mame-libretro", "mame-mame4all", "mastersystem",
                 "megadrive", "msx", "n64", "neogeo", "nes", "ngp", "ngpc", "pc", "ports", "psp", "psx", "scummvm",
                 "sega32x", "segacd", "sg-1000", "snes", "vectrex", "videopac", "wonderswan", "wonderswancolor",
                 "zmachine", "zxspectrum"]
    if console != "":
        if console in emulators:
            romfile = "/home/pi/RetroPie/roms/" + console + "/" + game
            if os.path.isfile(romfile):
                return True

#############################################################################################
# Return the full path of the rom
def get_rompath(console, game):
    # escape the spaces and brackets in rom filename
    game = game.replace(" ", "\ ")
    game = game.replace("(", "\(")
    game = game.replace(")", "\)")
    game = game.replace("'", "\\'")

    rompath = "/home/pi/RetroPie/roms/" + console + "/" + game
    return rompath

#############################################################################################
# Return the path of the emulator ready to be used later
def get_emulatorpath(console):
    path = "/opt/retropie/supplementary/runcommand/runcommand.sh 0 _SYS_ " + console + " "
    return path

#############################################################################################
# Kills the task of 'procnames', also forces Kodi to close if it's running
def killtasks(procnames):
    for proc in psutil.process_iter():
        if proc.name() in procnames:
            pid = str(proc.as_dict(attrs=['pid'])['pid'])
            name = proc.as_dict(attrs=['name'])['name']
            print("stopping... " + name + " (pid:" + pid + ")")
            subprocess.call(["sudo", "kill", "-15", pid])

    kodiproc = ["kodi", "kodi.bin"] # kodi needs SIGKILL -9 to close
    for proc in psutil.process_iter():
        if proc.name() in kodiproc:
            pid = str(proc.as_dict(attrs=['pid'])['pid'])
            name = proc.as_dict(attrs=['name'])['name']
            print("stopping... " + name + " (pid:" + pid + ")")
            subprocess.call(["sudo", "kill", "-9", pid])

#############################################################################################
# Returns True if the 'proc_name' process name is currently running
def process_exists(proc_name):
    ps = subprocess.Popen("ps ax -o pid= -o args= ", shell=True, stdout=subprocess.PIPE)
    ps_pid = ps.pid
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    for line in output.split("\n"):
        res = re.findall("(\d+) (.*)", line)
        if res:
            pid = int(res[0][0])
            if proc_name in res[0][1] and pid != os.getpid() and pid != ps_pid:
                return True
    return False

#############################################################################################
# Safely shuts-down the system
def shutdown():
    print("shutdown...\n")
    subprocess.call("sudo shutdown -h now", shell=True)

#############################################################################################
# Main program: input is 'action console game'                                              #
#                                                                                           #
# Possible actions are: run, stop and shutdown                                              #
#                                                                                           #
# Run will start the specified game, turn the tv on and to the right channel                #
# Stop will end the game if it was started through RetroCast, otherwise nothing will happen #
# Shutdown will shut down the system and the TV.                                            #
#############################################################################################

action = sys.argv[1]

if (sys.argv) > 3:
    console = sys.argv[2]
    game = sys.argv[3]

    # Run action -> Runs game if nothing is running.
    if action == "run":
        if valid_game(console, game):
            subprocess.call("echo \"on 0\" | cec-client -s -d 1", shell=True)  # Turn on TV
            subprocess.call("echo \"as\" | cec-client -s -d 1", shell=True)  # Set TV to the correct input channel
            procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                     "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                     "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                     "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                     "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                     "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                     "wolf4sdl", "solarus", "emulationstation", "emulationstatio"]
            killtasks(procnames)
            emulatorpath = get_emulatorpath(console)
            rompath = get_rompath(console, game)
            subprocess.call("sudo openvt -c 1 -s -f " + emulatorpath + rompath + "&", shell=True)
            subprocess.call("sudo chown pi -R /tmp", shell=True)  # ES needs permission as 'pi' to access this later
            time.sleep(2)
            subprocess.call("echo \" tx 10:47:52:65:74:72:6F:43:61:73:74 \" | cec-client -s -d 1", shell=True) # Set CEC name to RetroCast
        else:
            print("Not a valid game.\n")

# Stop action -> Stops game if it was started through RetroCast, else just leave it running.
if action == "stop":
    if process_exists("emulationstation"):
        print("Emulationstation is running...\n")
    else:
        procnames = ["retroarch", "ags", "uae4all2", "uae4arm", "capricerpi", "linapple", "hatari", "stella",
                     "atari800", "xroar", "vice", "daphne", "reicast", "pifba", "osmose", "gpsp", "jzintv",
                     "basiliskll", "mame", "advmame", "dgen", "openmsx", "mupen64plus", "gngeo", "dosbox", "ppsspp",
                     "simcoupe", "scummvm", "snes9x", "pisnes", "frotz", "fbzx", "fuse", "gemrb", "cgenesis", "zdoom",
                     "eduke32", "lincity", "love", "alephone", "micropolis", "openbor", "openttd", "opentyrian",
                     "cannonball", "tyrquake", "ioquake3", "residualvm", "xrick", "sdlpop", "uqm", "stratagus",
                     "wolf4sdl", "solarus"]
        killtasks(procnames)
        subprocess.call("echo \"standby 0\" | cec-client -s -d 1", shell=True) # Turn off TV

# Shutdown action -> Shuts down the system, regardless of what is running.
if action == "shutdown":
    subprocess.call("echo \"standby 0\" | cec-client -s -d 1", shell=True) # Turn off TV
    print("Shutting down...\n")
    subprocess.call("sudo shutdown -h now", shell=True) #Turn off system