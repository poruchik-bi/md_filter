from multiprocessing import Process
import os, sys
import time
import subprocess

test_video = "/home/er/workspace/md_filter/10.0.6.25_04_20220212124853446.mp4"

def duratioin_format(seconds):
    seconds = int(seconds)

    h = seconds // 3600
    m = (seconds // 60 ) % 60
    s = seconds % 60
    
    return f'{h:02d}:{m:02d}:{s:02d}'

class FFPlayer():
    def __init__(self):
        self.child_proc = None
    
    def __enter__(self): 
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback): 
        self.stop_player()

    def player(self, file, seconds):

        t = duratioin_format(seconds)

        print (f"Play file {file} ID# {os.getpid()}")
        cmd = f"ffplay -ss {t} {file}"
        
        os.system(cmd)

        
    def run_player(self, file, seconds):

        self.stop_player()

        self.child_proc = Process(target=self.player, args=(file, seconds)) 
        self.child_proc.start()
        
    def stop_player(self):
        if self.child_proc is not None:

            if sys.platform == "win32":
                os.system("taskkill /IM ffplay.exe")
            else:
                os.system("killall ffplay")

            self.child_proc.terminate()
            self.child_proc.join()
            
            self.child_proc = None

if __name__ == "__main__":

    with FFPlayer() as player:
        player.run_player(test_video, 100)
        time.sleep(20)

    print ("in parent process after child process join")
    print ("the parent's parent process: %s" % (os.getppid()))