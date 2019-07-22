from __future__ import print_function
from __future__ import division
import os
import subprocess
import time
import sys

from Stream_Parser import *


class Frame_Grabber(object):
    #ffmpeg -i http://jura:9981/stream/channel/?ticket= -q:a 0 -map a tmp/sample.mp3 -qscale:v 7 -vf fps=1 tmp/img%010d.jpg
    #ffmpeg -i {url} -f segment -segment_time {audiosegtime} -c copy {dirpath}audiofile%010d.aac -qscale:v 7 -vf fps={fps} {dirpath}img%010d.jpg
    FFMPEG_COMMAND_WITH_AUDIO = "ffmpeg -i {url} -f segment -segment_time 100 -c copy {dirpath}audiofile%010d.aac -qscale:v 7 -vf fps={fps} {dirpath}img%010d.jpg"
    FFMPEG_COMMAND_WITHOUT_AUDIO = "ffmpeg -i {url} -qscale:v {qscale} -vf fps={fps} {dirpath}img%010d.jpg"

    def __init__(self, frame_grabbing_timeout_seconds, frames_per_second, store_frames_to_path, channels_directory,
                 grab_audio=False):
        self.timeout = frame_grabbing_timeout_seconds
        self.store_directory = store_frames_to_path
        self.channels_directory = channels_directory
        self.stream_url = Stream_Parser.convert_stream_urls_to_dictionary(channels_directory)
        self.frames_per_second = frames_per_second

        self.qscale = 7

        self.grab_audio = grab_audio
        self.audio_segment_time = 100 #seconds
        if self.grab_audio:
            Frame_Grabber.FFMPEG_COMMAND = Frame_Grabber.FFMPEG_COMMAND_WITH_AUDIO
            print("Grabbing frames & audio")
        else:
            Frame_Grabber.FFMPEG_COMMAND = Frame_Grabber.FFMPEG_COMMAND_WITHOUT_AUDIO
            print("Grabbing only frames")

        print("Command is:")
        print(Frame_Grabber.FFMPEG_COMMAND)

        #list to store the running processes
        self.processes = []

    def __repr__(self):
        str_list = []
        for k in self.stream_url.keys():
            str_list.append("{} -> {}".format(k, self.stream_url[k]))
        return "\n".join(str_list)

    @staticmethod
    def ffmpeg_command(url, fps, dirpath, qscale):
        ffmpeg_command = Frame_Grabber.FFMPEG_COMMAND.format(url=url, fps=fps, dirpath=dirpath,
            qscale=qscale)
        return ffmpeg_command

    @staticmethod
    def concat_path(rootdir, streamdir):
        rootdir = Stream_Parser.check_path(rootdir)
        streamdir = Stream_Parser.check_path(streamdir)
        return rootdir+streamdir

    @staticmethod
    def create_dir(pathroot):
        pathroot =  Stream_Parser.check_path(pathroot)

        if not os.path.exists(pathroot):
            os.mkdir(pathroot)

    def grab_frames(self):
        outputdir = self.store_directory
        self.create_dir(outputdir)

        started = time.time()
        for stream, url in self.stream_url.items():
            fullpath = self.concat_path(outputdir, stream)
            self.create_dir(fullpath)
            ffmpeg = self.ffmpeg_command(url, self.frames_per_second, fullpath, self.qscale)
            print(ffmpeg)
            print("\n")
            print("-----------------------------------------------------------")
            print("RECORDING STARTED:")
            print(stream)
            print("-----------------------------------------------------------")
            print("\n")
            self.processes.append(subprocess.Popen("exec "+ffmpeg, shell=True, stdout=subprocess.PIPE))
            time.sleep(1)

        repeat = True
        while repeat:
            for p in self.processes:
                if (time.time() - started) > self.timeout:
                        repeat = False
                        print("STOP REPEATING")

                time.sleep(10)
            print("Seconds passed: {}".format(time.time()-started))
            print("Seconds left: {}".format(self.timeout-(time.time()-started)))

        # kill subprocess
        print("killing processes")
        for p in self.processes:
            p.kill()
            print("terminated")

if __name__=="__main__":
    fg = Frame_Grabber(frame_grabbing_timeout_seconds=36000,
                       frames_per_second=1,
                       channels_directory="RTL4/",
                       store_frames_to_path=
                       "/media/evan/HardDisk/GrabFrames/RTL4_good",
                       grab_audio=False)
    fg.qscale=11
    fg.grab_frames()
