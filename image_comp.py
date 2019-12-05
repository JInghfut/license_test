# compare the rendered test results to the expected results (using sci-kit image lib)

import skimage.external.tifffile as tif
from skimage.measure import compare_ssim as ssim
from skimage.transform import rescale
import numpy as np
import os
from math import isnan, isinf
import time
import logging
import imageio

def read_image(image_file):
    return_image = ''

    if os.path.isfile(image_file):
        if image_file.endswith('.tif'):
            return_image = tif.imread(image_file)
        else:
            # else test image is an EXR file, so use imageio to read and convert to PIL image (same structure as a numpy array)
            return_image = imageio.imread(image_file)
            return_image = np.array(return_image)
    else:
        logging.info('Image file not readable?  Waiting then re-trying...')
        for i in range(4):
            time.sleep(3)
            if os.path.isfile(image_file):
                if image_file.endswith('.tif'):
                    return_image = tif.imread(image_file)
                    break
                else:
                    return_image = imageio.imread(image_file)
                    return_image = np.array(return_image)
                    break

    return return_image

def compare_image_files(test_results_name, exp_results_name):

    # time.sleep(1)
    test_im = ''
    exp_im = ''
    tolerance = 0.3

    test_im = read_image(test_results_name)

    exp_im = read_image(exp_results_name)

    # this would be a better test if testing the images becomes necessary:
    # check that the image dimensions match:
    # if not test_im.shape == exp_im.shape:
    #     return {'success': False, 'error_status': 'ONE OR MORE IMAGE FILES READ INCORRECTLY!'}

    all_close = np.allclose(test_im, exp_im, atol=tolerance)

    if all_close:
        return {'success': True}

    else:
        err_status = pixel_comp(test_im, exp_im, tolerance)

        return {'success': False, 'error_status': err_status}

# Compare pixel-by-pixel with the same process as image_utils and fimage
def pixel_comp(test_im, exp_im, tolerance):

    msg = None
    n_bad = 0
    n_bad10x = 0
    n_bad100x = 0
    n_badfloat = 0
    worst_diff = 0
    worst_x = -1
    worst_y = -1
    worst_ch = -1
    abstol = tolerance
    reltol = 1e-8

    # log the 'Error Severity' of the error:
    # The closer to 1 the 'Error Severity' the less noticeable the error (based on the SSIM function)
    # if statement because computation of ssim on smaller system crashes due to memoryError!
    # tests if height <= 1080 (HD)
    if exp_im.shape[0] <= 1080:
        error_ssim = ssim(exp_im, test_im, multichannel=True, data_range=test_im.max() - test_im.min())

    # else rescale the test images so that the computer has enough ram to process...
    # note that w/ rescaling the diffs will be measured differently, as this is a rough metric for 'severity', it should be fine
    else:
        # note currently scaling to 1/2 size, could probably get away with scaling to 3/4, or higher for better accuracy
        logging.info('Scaling down image by 0.5 because they are too large.')
        exp_scale = rescale(exp_im, 0.5, mode='reflect', preserve_range=True)
        test_scale = rescale(test_im, 0.5, mode='reflect', preserve_range=True)

        error_ssim = ssim(exp_scale, test_scale, multichannel=True, data_range=test_scale.max() - test_scale.min())

    tmp = 1 - error_ssim
    E_S = tmp * 10
    logging.info('\nThe Error Severity = ' + str(E_S))

    for y in range(test_im.shape[0]):
        for x in range(test_im.shape[1]):

            for ch in range(test_im.shape[2]):

                myval = test_im[y][x][ch]
                otherval = exp_im[y][x][ch]

                if isnan(myval) or isnan(otherval):
                    n_bad += 1
                    n_badfloat += 1
                    if n_bad == 1:
                        msg = "Pixel %d,%d ch%d: saw NaN, mine=%f, other=%f" % \
                              (x, y, ch,
                               test_im[y][x][ch],
                               exp_im[y][x][ch])
                if isinf(myval) or isinf(otherval):
                    n_bad += 1
                    n_badfloat += 1
                    if n_bad == 1:
                        msg = "Pixel %d,%d ch%d: saw INF, mine=%f, other=%f" % \
                              (x, y, ch,
                               test_im[y][x][ch],
                               exp_im[y][x][ch])
                if not _isclose(myval, otherval, abstol, reltol):
                    n_bad += 1
                    diff = abs(myval - otherval)
                    if diff > worst_diff:
                        worst_diff, worst_x, worst_y, worst_ch = diff, x, y, ch
                    if n_bad == 1 and n_badfloat == 0:
                        msg = "Pixel %d,%d ch%d mismatch: mine=%g, other=%g" % \
                              (x, y, ch,
                               test_im[y][x][ch],
                               exp_im[y][x][ch])
                    if not _isclose(myval, otherval, abstol * 10.0, reltol):
                        n_bad10x += 1
                    if not _isclose(myval, otherval, abstol * 100.0, reltol):
                        n_bad100x += 1
    if n_bad > 0:
        msg += "\n Total: %d bad values, abstol=%g" % (n_bad, abstol)
        msg += "\n Worst diff=%g at %d,%d ch%d" % (worst_diff, worst_x, worst_y, worst_ch)
        if n_bad10x:
            msg += "\n %d bad values above 10x tolerance, %d above 100x" % \
                   (n_bad10x, n_bad100x)
        if n_badfloat:
            msg += "\n %d BAD FLOAT VALUES (NaN, INF)" % (n_badfloat)
        msg += "\n Error Severity: {0:.2f}".format(E_S)

    return {'message': msg, 'n_bad': n_bad,
            'n_bad10x': n_bad10x, 'n_bad100x': n_bad100x,
            'n_badfloat': n_badfloat,
            'maxdiff': worst_diff}


def _isclose(a, b, abstol, reltol=1e-8):
    """Returns true if a is "close" to b for the given tolerances.
    abstol is the maximum absolute difference;
    reltol is the maximum relative difference.
    This is the algorithm used by numpy.
    """
    #if type(a) not in (type(0.0), type(0)) :
    #    raise (TypeError, "Type of a: %s is %s, should be float"%(a, type(a)))
    #if type(b) not in (type(0.0), type(0)) :
    #    raise (TypeError, "Type of b: %s is %s, should be float"%(a, type(a)))
    #if isnan(a) and isnan(b):
    #    return True
    #if isnan(a) or isnan(b):
    #    return False
    return abs(a - b) <= (abstol + reltol * abs(b))
