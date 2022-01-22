from pathlib import Path
from pqdm.threads import pqdm
from rich.console import Console
from shutil import copy2
from absl import app, flags
from absl.flags import FLAGS
import os
from itertools import repeat


flags.DEFINE_string('original', "w8_cvat", 'Input directory inside which cvat-yolo annotations have been extracted')


def cpy(src, dst):
    '''
    copies the file from src to dst

    Parameters
    ----------
    src : str
        source file which needs to be copied
    dst : str
        destination folder inside which needs to be copied
    '''    
    copy2(src, dst)




def main(argv):
    base = Path(FLAGS.original)

    # ==========================================================================
    #                             assert that paths exist                                  
    # ==========================================================================
    assert (base / "obj_train_data").exists() , "obj_train_data must exist in the original directory downloaded from cvat-yolo"
    assert (base / "obj.data").exists() , "obj.data must exist in the original directory downloaded from cvat-yolo"
    assert (base / "obj.names").exists() , "obj.names must exist in the original directory downloaded from cvat-yolo"
    assert (base / "train.txt").exists() , "train.txt must exist in the original directory downloaded from cvat-yolo"

    classes = [k.strip()  for k in open(str(base / "obj.names"), "r").readlines()]
    Console().rule(title=f'[bold cyan]got  [bold green]{len(classes)} from obj.names', characters='-', style='bold yellow')
    with open("mosaic_augmentation_on_yolo_format/w9/obj.names", "w") as f:
        f.writelines(classes)
    Console().rule(title=f'[color(128)]written  [bold red]obj.names to [yellow]mosaic_augmentation_on_yolo_format/w9/obj.names', characters='-', style='bold magenta')
    # with open("mosaic_augmentation_on_yolo_format/w9/obj.data", "r") as f:
    #     obj_data = f.readlines()
        
    # obj_data = [k.strip() for k in obj_data]
    # obj_data[0] = "classes=" + str(len(classes))
    # with open("mosaic_augmentation_on_yolo_format/w9/obj.data", "w") as k:
    #     k.writelines(obj_data)
    images = base / "obj_train_data"
    # copy all annots + images
    to_cpy = [k for k in images.iterdir() if k.is_file()]

    args = [[k.as_posix(), v] for k, v in zip(to_cpy, repeat("mosaic_augmentation_on_yolo_format/w9/data"))]
    Console().log(args)
    pqdm(args, to_cpy, desc="Copying files", argument_type='args', n_jobs=12)
    

if __name__ == '__main__':
    app.run(main)