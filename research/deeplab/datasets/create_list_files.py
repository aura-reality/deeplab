import argparse
import os
import random
from math import floor

import data_generator

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", help="the input directory")
    ap.add_argument("output_dir", help="the input directory")
    ap.add_argument("--name", required=True, help="the dataset name (used for validation)")
    ap.add_argument("-p", "--train_percent", default="0.9", help="the percentage of data to use in training (the remaining will be used in validation)")
    args = ap.parse_args()
    input_dir = args.input_dir
    output_dir = args.output_dir
    train_percent = float(args.train_percent)
    name = args.name

    dataset_info = data_generator._DATASETS_INFORMATION.get(name)
    if not dataset_info:
        raise Exception("Unknown name '%s'. Either fix the name or add it to data_generator.py" % name)

    if not os.path.isdir(output_dir):
        print("Creating folder: %s" % output_dir)
        os.mkdir(output_dir)
    else:
        raise Exception("Folder '%s' already exists. Delete the folder and re-run the code!" % output_dir)

    files = os.listdir(input_dir)
    random.shuffle(files)
    train_size = int(floor(len(files) * train_percent))
    val_size = len(files) - train_size

    actual_train_size = dataset_info.splits_to_sizes.get('train')
    actual_val_size = dataset_info.splits_to_sizes.get('val')

    if train_size is not actual_train_size or val_size is not actual_val_size:
        raise Exception("""The 'train' and 'val' sizes are incorrectly set in
                        'data_generator.py'. Use %s and %s and then RERUN THIS
                        SCRIPT! (got %s and %s)"""
                         % (int(train_size), int(val_size), actual_train_size,
                            actual_val_size))

    def make_txt_file(named, with_names):
        dest = os.path.join(output_dir, named)
        with open(dest, 'w') as file:
            file.write('\n'.join([f.replace(".png","").replace(".jpg","") for f
                                  in with_names]))
            print("Generated %s" % dest)

    make_txt_file("train.txt", files[:train_size])
    make_txt_file("val.txt", files[train_size:])
