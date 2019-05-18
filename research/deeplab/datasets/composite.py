import os
import math
import random
import argparse

import cv2 as cv
import numpy as np
from tqdm import tqdm as progress_bar

from util import parse_image_path, list_images

def process(fg_path, a_path, bg_path):
    fg = cv.imread(fg_path)
    bg = cv.imread(bg_path)
    a = cv.imread(a_path, 0)

    if fg is None or a is None or bg is None:
        if fg is None:
            bad = fg_path
        elif a is None:
            bad = a_path
        else:
            bad = bg_path
        raise Exception("Could not read image: %s" % bad)

    h, w = fg.shape[:2]
    bh, bw = bg.shape[:2]
    wratio = w / float(bw)
    hratio = h / float(bh)
    ratio = wratio if wratio > hratio else hratio
    if ratio > 1:
        bg = cv.resize(src=bg, dsize=(int(math.ceil(bw * ratio)),
                                      int(math.ceil(bh * ratio))), interpolation=cv.INTER_CUBIC)
    return composite4(fg, bg, a, w, h)

def composite4(fg, bg, a, w, h):
    fg = np.array(fg, np.float32)
    bg_h, bg_w = bg.shape[:2]
    x = 0
    if bg_w > w:
        x = np.random.randint(0, bg_w - w)
    y = 0
    if bg_h > h:
        y = np.random.randint(0, bg_h - h)
    bg = np.array(bg[y:y + h, x:x + w], np.float32)
    alpha = np.zeros((h, w, 1), np.float32)
    alpha[:, :, 0] = a / 255.
    im = alpha * fg + (1 - alpha) * bg
    im = im.astype(np.uint8)
    return im

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("--fg", required=True, help="the directory of foregrounds")
    ap.add_argument("--bg", required=True, help="the directory of backgrounds")
    ap.add_argument("--mask", required=True, help="the directory of masks")
    ap.add_argument("-o", required=True, help="the output directory")
    ap.add_argument("-n", default=1, help="the number of backgrounds per foreground")

    args = ap.parse_args()

    fg_dir = args.fg
    bg_dir = args.bg
    output_dir = args.o
    mask_dir = args.mask
    n = int(args.n)

    if not os.path.isdir(output_dir):
        print("Creating folder: %s" % output_dir)
        os.mkdir(output_dir)
    else:
        raise Exception("""Folder already exists. Delete the folder and re-run the
                        code! 'rm -rf %s'""" % output_dir)

    fgs = list_images(args.fg)
    bgs = list_images(args.bg)

    if n * len(fgs) > len(bgs):
        raise Exception("""There are not enough backgrounds to satisfy %s per
                        foreground! (There can be at most %.2f per foreground).
                        Use `-n 0` to try your best."""
                        % (n, len(fgs) / float(len(bgs))))

    try_your_best = n == 0
    if try_your_best:
        n = 1

    random.shuffle(bgs)

    i = 0
    break_outer = False
    for fg in progress_bar(fgs):
        fg_name, extension = parse_image_path(fg)

        for _ in range(n):
            if try_your_best and i >= len(bgs):
                break_outer = True
                break
                
            bg = bgs[i]
            i = i + 1

            fg_path = os.path.join(fg_dir, fg)
            bg_path = os.path.join(bg_dir, bg)
            a_path = os.path.join(mask_dir, fg)

            im = process(fg_path, a_path, bg_path)

            bg_name, _ = parse_image_path(bg)
            cv.imwrite(os.path.join(output_dir, "%s_%s.%s" % (fg_name, bg_name,
                                                           extension)), im)

        if break_outer:
            break
