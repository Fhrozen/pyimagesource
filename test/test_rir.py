#!/usr/bin/env python3

import sys

import pyimagesource
import numpy as np
import soundfile

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def main():
    wavdata, samplerate = soundfile.read('./test/thriller.wav')
    # Room Dimensions in X, Y, Z (m)
    rir_file = './test/test_rir_np23.npy'
    my_room = np.asarray([[3, 4, 2.5]])

    # Mic positions in X, Y, Z (m)
    my_mics = np.asarray([[1.6, 1, 1.3],
                          [1.4, 1, 1.3],
                          [1.2, 1, 1.3]])
    my_sources = np.asarray([[1, 3, 1.7]])

    if True:
        # Generates RIR and saves it
        my_rev = [60, 0.4]
        # my_rev = [20, 0.15]
        my_weights = np.asarray([[0.6, 0.9, 0.5, 0.6, 1.0, 0.8]])
        print("Evaluating Anechoic ir")
        my_rir = pyimagesource.Room_Impulse_Response(samplerate, my_room, my_mics, 
                                               my_sources, [60, 0.0], my_weights, verbose=True,
                                               processes=3)

        rirs = my_rir.bank()

        print("Evaluating Echoic ir")
        my_rir = pyimagesource.Room_Impulse_Response(samplerate, my_room, my_mics, 
                                               my_sources, my_rev, my_weights, verbose=True,
                                               processes=3)

        rirs = my_rir.bank()
        np.save(rir_file, rirs)
    else:
        rirs = np.load(rir_file)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(my_sources[:, 0], my_sources[:, 1], my_sources[:, 2], c='b', marker='^', label='Sources')
    ax.scatter(my_mics[:, 0], my_mics[:, 1], my_mics[:, 2], c='r', marker='o', label='Microphones')
    ax.set_xlim(0, my_room[0,0])
    ax.set_ylim(0, my_room[0,1])
    ax.set_zlim(0, my_room[0,2])
    ax.set_xlabel('X axis (m)')
    ax.set_ylabel('Y axis (m)')
    ax.set_zlabel('Z axis (m)')
    ax.legend()
    reverberated = pyimagesource.audiodata(rirs, wavdata)

    plt.figure()
    plt.plot(reverberated.T)
    plt.savefig('./test/reverberated.png')
    # plt.show()
    soundfile.write('./test/test_thriller.wav', reverberated.T, samplerate)


if __name__ == '__main__':
    main()
