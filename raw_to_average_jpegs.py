#! /usr/bin/env python
#
# Tested on Macs. First run `brew install ufraw exiftool`

import argparse
import glob
import multiprocessing as mp
import os
import subprocess


def parseArgs():
    desc = 'Auto-white-balance raw images and create average-sized JPEG files with their EXIF info.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--path', dest='imagesPath', default=os.getcwd(),
                        help='Sets the path containing the DNG images. Default is the current ' + \
                             'working directory, which is: %(default)s')
    return parser, parser.parse_args()


def processFiles(fname):
    subprocess.check_call(['ufraw-batch', '--wb=auto', '--overwrite',
                     '--size=2048', '--out-type=jpeg', fname])
    subprocess.check_call(['exiftool', '-overwrite_original', '-q', '-x', 'Orientation',
                     '-TagsFromFile', fname, fname.replace('.DNG', '.jpg')])


def workingProgramCheck(prog):
    '''Checks whether the program is accessible on the system.'''
    try:
        subprocess.check_call(['which', '-s', prog])
    except Exception:
        raise Exception(prog + ' is not accessible on the system.')


def main():
    parser, args = parseArgs()

    # Check whether ufraw and exiftool are working properly.
    workingProgramCheck('ufraw-batch')
    workingProgramCheck('exiftool')

    pool = mp.Pool(mp.cpu_count())

    for fname in glob.glob(os.path.normpath(os.path.join(args.imagesPath, '*.DNG'))):
        pool.apply_async(processFiles, [fname])

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
