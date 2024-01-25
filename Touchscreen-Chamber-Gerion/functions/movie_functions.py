from psychopy import visual, prefs
# prefs.general['audioLib'] = ['pyo']
prefs.general['audioLib'] = ['PTB']
prefs.general['audioDevice'] = ['Built-in Output']
from psychopy import sound
from os import path

import sys
import os

# FFMPEG is expected in this location:
ffmpeg_path = r'C:\FFMpeg'

# This is an overwrite in case the user is not an admin that can add this permanently to the environmental variables
sys.path.append(path.join(ffmpeg_path, 'bin'))
sys.path.append(path.join(ffmpeg_path, 'bin', 'ffmpeg.exe'))

# os.environ['IMAGEIO_FFMPEG_EXE'] = r'C:\Users\linde\Desktop\FFMpeg\bin\ffmpeg.exe'
os.environ['IMAGEIO_FFMPEG_EXE'] = path.join(ffmpeg_path, 'bin', 'ffmpeg.exe')


def load_movie(win, file_path, noAudio=True, opacity=1., pos=(0, 0), setup_scale=2, loop=True):
    return visual.MovieStim3(win, file_path, size=(500 / setup_scale, 500 / setup_scale), pos=pos, noAudio=noAudio,
                             opacity=opacity, loop=loop)
#


def load_next_stimulus(target_mov, distractor_mov, target_path, distractor_path, target_side_left=True, distractor_opacity=1.,
                       setup_scale=2):
    # if target_side_left:
    #     target_position = -250 / setup_scale
    #     distractor_position = 250 / setup_scale
    # else:
    #     distractor_position = -250 / setup_scale
    #     target_position = 250 / setup_scale
    # #

    if target_side_left:
        target_position = - target_mov.size[0] / 2
        distractor_position = distractor_mov.size[0] / 2
    else:
        distractor_position = - distractor_mov.size[0] / 2
        target_position = target_mov.size[0] / 2
    #

    if distractor_mov is not None:
        distractor_mov.loadMovie(distractor_path)
    target_mov.loadMovie(target_path)

    target_mov.setPos([target_position, 0])
    if distractor_mov is not None:
        distractor_mov.setPos([distractor_position, 0])

    target_mov.setOpacity(1)
    if distractor_mov is not None:
        try:
            # print(distractor_opacity)
            distractor_mov.setOpacity(distractor_opacity)
        except:
            # print('Overwrote Dist. contrast')
            distractor_mov.setOpacity(1)
        #
    # distractor_mov.opacity = distractor_opacity
    # print('Opacity: ', distractor_mov.opacity)

    target_mov.setAutoDraw(True)
    if distractor_mov is not None:
        distractor_mov.setAutoDraw(True)

    # target_mov.play()
    # distractor_mov.play()
#
