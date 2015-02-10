"""
    pyVideo
    Simple command line script that converts an input video and
    into another format or just an audio track.
"""
__author__ = "DarMat"

import argparse
import os
import subprocess


def Wav(): return '-ar 48000 -ac 2 -vn'

def Mp3(): return ''

def Avi(): return '-ar 22050 -r 30 -s 480x360 -vcodec flv -qscale 9.5'
    
def Ogg(): return '-strict -2 -acodec vorbis -aq 60'
    
def Mpg(): return '-target ntsc-dvd -aspect 4:3'

def Default(): return 'error'

def GetOptions(format):
    try:
        return {'wav': Wav,
                'mp3': Mp3,
                'avi': Avi,
                'ogg': Ogg,
                'mpg': Mpg}[format]
    except KeyError:
        return Default


def ParseArgs():
    """ 
    Routine that parses the input arguments and returns them.
    """
    parser = argparse.ArgumentParser(description='Extract the audio track from a video')
    parser.add_argument('-i', '--input', 
                        dest='input',
                        metavar='FILE',
                        help='path to the video file to extract from',
                        required=True)
    parser.add_argument('-f', '--format', 
                        dest='format',
                        metavar='FORMAT',
                        help='format of output audio file',
                        required=True)
    parser.add_argument('-b', '--bitrate', 
                        dest='bitrate',
                        metavar='BITRATE',
                        default='320k',
                        help='specify the mp3 bitrate',
                        required=False)
    args = parser.parse_args()    
    return args.input, args.format, args.bitrate


def GetCommandOptions(audio_format, bitrate):
    """
    Helper routine that formats a string with the optional argument for the
    ffmpeg command, every output format will require a different set of options.
    """
    return '-ab {} {}'.format(bitrate, GetOptions(audio_format)())


def Convert():
    """
    This routines fetches the input argument, format the command string
    and finally execute the ffmpeg command.
    """
    input, audio_format, bitrate = ParseArgs()
    
    audio_format = audio_format.lower()
    _, file = os.path.split(input)
    file_name, __ = os.path.splitext(file)
    options = GetCommandOptions(audio_format, bitrate)
    
    command = 'ffmpeg -i {} {} {}.{}'.format(input, options, file_name, audio_format)
    
    if 'error' not in command:
        subprocess.call(command, shell=True)
    else:
        print 'Output file format not supported.'
    

if __name__ == '__main__':
    """ Main """
    Convert()
