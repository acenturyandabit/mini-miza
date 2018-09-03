#!/usr/bin/env python3
import subprocess
import sys
import time
import os

# --- set the application below
apps = ["evolution",'']
pids = ["7070"]
# ---

minitime = (int(sys.argv[1])/2)*2
FNULL = open(os.devnull, 'w')
def get(cmd):
    # helper function
    try:
        return subprocess.check_output(cmd,stderr=FNULL).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        return None


t = {}

while True:
    time.sleep(2)
    # first check if app is runing at all (saves fuel if not)
    for app in apps:
        _pids = get(["pgrep", app]).splitlines()
        for pid in _pids:
            pid=str(int(pid))
            # if app is running, look up its windows
            windows = get(["xdotool", "search", "--all", "--pid", pid,".+"])
            if not windows is None:
                windows=windows.splitlines()
                # Increment timer on all windows we care about
                for w in windows:
                    try:
                        t[w] += 2
                        # if timer for window exceeds minimise time, minimise the window.
                        if t[w]==minitime:
                            subprocess.Popen(["xdotool", "windowminimize", w])
                    except KeyError:
                        t[w]=2  
                #If window is focused, reset its timer
                if get(["xdotool", "getactivewindow"]) in windows:
                    t[get(["xdotool", "getactivewindow"])] = 0
    # same but for custom PIDs
    for pid in pids:
        pid=str(int(pid))
        # if app is running, look up its windows
        windows = get(["xdotool", "search", "--all", "--pid", pid,".+"])
        if not windows is None:
            windows=windows.splitlines()
            # Increment timer on all windows we care about
            for w in windows:
                try:
                    t[w] += 2

                    # if timer for window exceeds minimise time, minimise the window.
                    if t[w]==minitime:
                        subprocess.Popen(["xdotool", "windowminimize", w])
                except KeyError:
                    t[w]=2  
            #If window is focused, reset its timer
            if get(["xdotool", "getactivewindow"]) in windows:
                t[get(["xdotool", "getactivewindow"])] = 0