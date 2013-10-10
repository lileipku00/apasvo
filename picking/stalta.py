# encoding: utf-8
'''
@author:     Jose Emilio Romero Lopez

@copyright:  2013 organization_name. All rights reserved.

@license:    LGPL

@contact:    jemromerol@gmail.com

  This file is part of AMPAPicker.

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import numpy as np

from findpeaks import find_peaks


def sta_lta(x, fs, threshold=None, sta_length=5., lta_length=100.,
            peak_window=1.):
    # Check arguments
    if fs <= 0:
        raise ValueError("fs must be a positive value")
    if sta_length <= 0:
        raise ValueError("sta_length must be a positive value")
    if lta_length <= 0:
        raise ValueError("lta_length must be a positive value")
    if sta_length >= lta_length:
        raise ValueError("lta_length must be greater than sta_length")
    sta = sta_length * fs
    lta = lta_length * fs
    peak_window = int(peak_window * fs / 2.)
    x_norm = np.abs(x - np.mean(x))
    cf = np.zeros(len(x))
    for i in xrange(len(x_norm)):
        sta_to = int(min(len(x_norm), i + sta + 1))
        lta_to = int(min(len(x_norm), i + lta + 1))
        cf[i] = np.mean(x_norm[i:sta_to]) / np.mean(x_norm[i:lta_to])
    event_t = find_peaks(cf, threshold, order=peak_window * fs)
    return event_t, cf


class StaLta(object):

    def __init__(self, sta_length=10.0, lta_length=600.0, **kwargs):
        super(StaLta, self).__init__()
        self.sta_length = sta_length
        self.lta_length = lta_length
        self.name = 'STA-LTA'

    def run(self, x, fs, threshold=None, peak_window=1.0):
        et, cf = sta_lta(x, fs, threshold=threshold,
                         sta_length=self.sta_length,
                         lta_length=self.lta_length,
                         peak_window=peak_window)
        return et, cf
