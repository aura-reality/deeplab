# How to train to mask

#### -1. Set the dataset name and location of the github dir
```bash
# Set these two variables
DATASET_NAME=alpha_matting
DEEPLAB_HOME=/your/local/path/to/this/repo
FG=/your/local/path/to/foregrounds
BG=/your/local/path/to/backgrounds
MASK=/your/local/path/to/masks

# Compute these
DATASET_LOCATION=$DEEPLAB_HOME/research/deeplab/aura/data/$DATASET_NAME
COMPOSITE=$DATASET_LOCATION/composite
LISTS=$DATASET_LOCATION/training-lists
SEGMENTATION=$DATASET_LOCATION/segmentation
TFRECORD=$DATASET_LOCATION/tfrecord
SCRIPTS=$DEEPLAB_HOME/research/deeplab/datasets
```

#### 0. Setup a virtualenv
```bash
cd $DEEPLAB_HOME/research/deeplab/aura
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 1. Convert masks to segmentation files
```bash
python $SCRIPTS/masks-to-segmentations.py $MASK $SEGMENTATION
```

A pixel value of 0 is background, and 1 is foreground. That's impossible to visualize. To visualize, use the `--debug` flag to multiply everything by 128.
```bash
python $SCRIPTS/masks-to-segmentations.py $MASK $SEGMENTATION --debug
open ${SEGMENTATION}_debug
```

#### 2. Composite (locally)
By default, one background per foreground
```
python $SCRIPTS/composite.py --fg $FG --bg $BG --mask $MASK -n 1 -o $COMPOSITE
```

#### 3. Create the training and validation file-name lists
```bash
cd $DEEPLAB_HOME/research/deeplab/datasets
python create_list_files.py --name $DATASET_NAME $COMPOSITE $LISTS
```

*(To skip compositing, just put your files at `$COMPOSITE`, e.g. `mv $FG $COMPOSITE`)*

#### 4. Convert files to TF Records
```
cd $DEEPLAB_HOME/research/deeplab/datasets
mkdir -p $TFRECORD
python build_voc2012_data.py \
  --image_folder=$COMPOSITE \
  --semantic_segmentation_folder=$SEGMENTATION \
  --list_folder=$LISTS \
  --image_format=png \
  --output_dir=$TFRECORD
```

*Check on the results:*
```
open $COMPOSITE
```

#### 4. Run training
TODO

## TODO
* Crop around the intermediate region
* Assume users would give "object in circle"
