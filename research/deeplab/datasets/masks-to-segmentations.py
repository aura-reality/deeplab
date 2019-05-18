import argparse
import os

from PIL import Image
from tqdm import tqdm as progress_bar
import numpy as np

from util import list_images

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", help="the input directory")
    ap.add_argument("output_dir", help="the output directory")
    ap.add_argument("--debug", action='store_true', help="create debuggable output")
                    
    args = ap.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    debug = bool(args.debug)

    if not os.path.isdir(output_dir):
        print("Creating folder: %s" % output_dir)
        os.mkdir(output_dir)
    else:
        raise Exception("""Folder already exists. Delete the folder and re-run the
                        code! 'rm -rf %s'""" % output_dir)

    label_files = list_images(input_dir)

    for l_f in progress_bar(label_files):
        input_path = os.path.join(input_dir, l_f)
        arr = np.array(Image.open(input_path).convert("L")) # "L" ==> greyscale
        if len(arr.shape) != 2:
            raise Exception("For '%s', expected a greyscale image. Its shape was %s" %
                            (input_path, str(arr.shape)))

        # '0' is background and '1' is foreground
        arr = (arr > 128)
        arr.dtype = np.uint8
        if debug:
            arr = arr * 128
            output_dir = output_dir + "_debug"
        Image.fromarray(arr).save(os.path.join(output_dir, l_f))
