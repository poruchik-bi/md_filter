from multiprocessing import Process
import os, sys
import time
import threading

test_video = "input.mp4"

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

        binary = "ffplay.exe" if sys.platform == "win32" else "ffplay"
        
        cmd = f"{binary} -x 1280 -ss {t} {file}"

        print("cmd: ", cmd)

        os.system(cmd)

        
    def run_player(self, file, seconds):

        self.stop_player()

        self.child_proc = threading.Thread(target=self.player, args=(file, seconds,))
        self.child_proc.start()
        
    def stop_player(self):
        if self.child_proc is not None:

            if sys.platform == "win32":
                os.system("taskkill /IM ffplay.exe")
            else:
                os.system("killall ffplay")

            self.child_proc.join()
            
            self.child_proc = None

if __name__ == "__main__":

    with FFPlayer() as player:
        player.run_player(test_video, 100)
        time.sleep(20)

    print ("in parent process after child process join")
    print ("the parent's parent process: %s" % (os.getppid()))