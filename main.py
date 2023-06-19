# Author: Matteo Del Grosso
# Date: 18.6.2023
# State: In progress
#
# Problem/Motivation:
#   When migrating all image metadata from Capture One Pro to Lightroom Classic (LrC), the following problem has occurred:
#   LrC does not update the metadata of an image if the xmp metadata file is "older" than the corresponding image file.
#
# Solution:
#   Find all image files in the photo archive and update the timestamp of the associated xmp metadata file to the current date/time.
#   This will ensure that the metadata xmp file has a later modified date/time than the associated image file, thus Lightroom Classic
#   will read and update the metadata from the xmp file. The update may occur automatically by LrC or when the corresponding command is given.
#
# Procedure:
#   Iterate over all image files in photo archive and identify different types of images files and their associate xmp metadata xmp-file
#
# Image file types (file extensions) considered (case of extension is not relevant):
#   NEF - Nikon RAW files
#   DNG - Digital Negative RAW files
#   RW2 - Panasonic Lumix RAW files
#   RAF - Fujifilm RAW files
#   JPG - JPEG files

from collections import Counter
import os
from pathlib import Path


photo_root_folder: Path = Path("e:/photo/2023")
skip_folders: tuple[Path] = ("scan", "slides")
image_type_dict = {"dng": 0, "nef": 0, "raf": 0, "rw2": 0, "jpg": 0, "tif": 0}
image_type_count = Counter(image_type_dict)
image_type_count_with_xmp = Counter(image_type_dict)
image_type_count_without_xmp = Counter(image_type_dict)
missing_xmp_path_list: set[str] = set()


def main():
    total_file_count_per_folder: int = 0
    total_skipped_folder_count: int = 0
    for dir_path, dir_names, files in os.walk(photo_root_folder):
        # skip some folders
        if len(Path(dir_path).parts) > 2 and Path(dir_path).parts[2] in skip_folders:
            print(f"Skipping {dir_path}")
            total_skipped_folder_count += 1
            continue
        total_file_count_per_folder += len(files)
        # print(f"{dir_path}: {total_file_count} files")
        if total_file_count_per_folder == 0:
            continue
        for file in files:
            file_type: str = Path(file).suffix.lower()[1:]
            if file_type in image_type_count.keys():
                image_type_count[file_type] += 1
                image_xmp_file: Path = Path(dir_path) / Path(file).with_suffix(".xmp")
                if image_xmp_file.exists():
                    # image_xmp_file.touch()
                    image_type_count_with_xmp[file_type] += 1
                else:
                    image_type_count_without_xmp[file_type] += 1
                    missing_xmp_path_list.add(dir_path)
        # stats per image type
        print(f"{dir_path}: {total_file_count_per_folder} files total")
        for image_type, count in image_type_count.items():
            print(
                f"{image_type}: {count} (missing xmp: {image_type_count_without_xmp[image_type]})"
            )
            image_type_count[image_type] = 0
            image_type_count_without_xmp[image_type] = 0
        total_file_count_per_folder = 0
    # sanity check
    # assert (
    #     image_type_count_with_xmp.total() + image_type_count_without_xmp.total()
    #     == image_type_count.total()
    # ), "Image count error"

    # general stats
    print("\nStats")
    print(f"Total files: {total_file_count_per_folder}")
    print(f"Skipped folders: {skip_folders} count={total_skipped_folder_count}")
    print(f"Total number of images: {image_type_count.total()}")
    print(f"Total images with xmp files: {image_type_count_with_xmp.total()}")
    print(f"Total images without xmp files: {image_type_count_without_xmp.total()}")

    # stats per image type
    for image_type, count in image_type_count.items():
        print(
            f"{image_type}: {count} (missing xmp: {image_type_count_without_xmp[image_type]})"
        )

    print("Missing xmp files in path:")
    for path in missing_xmp_path_list:
        print(path)


if __name__ == "__main__":
    main()
