#!/usr/bin/python
import csv
import glob
from nif_walker import walk_nif
import os
import sys
import tarfile

RELEASE_PATH = "uixr-assets-cc0-1.0.tar"
ASSET_PATH = "../../../Private"


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def get_filename(string):
    return os.path.basename(string.replace("\\", "/"))


with open("Manifests/UIXR.manifest") as f:
    uixr_data = csv.DictReader(f)
    tar_ball = tarfile.open(RELEASE_PATH, "w:")
    spinner = spinning_cursor()
    additional_assets = []
    print("Gathering assets: ")
    for row in uixr_data:
        if row.get('license').lower() == 'cc0':
            sys.stdout.write("\033[K")
            sys.stdout.write(next(spinner))
            sys.stdout.write(" [{0}]".format(row.get('asset')))
            sys.stdout.flush()
            sys.stdout.write('\r\b')
            file_path = os.path.join(ASSET_PATH, row.get('asset'))
            tar_ball.add(file_path, row.get('asset'))

            # check that we have all related assets
            nif_assets = walk_nif(nif_path=file_path, use_stdout=False)
            for asset_string in nif_assets:
                for asset in asset_string.split(', '):
                    additional_assets.append(get_filename(asset))

    additional_assets = set(additional_assets)

    # remove blank entry in set
    if '' in additional_assets:
        additional_assets.remove('')

    print("Gathering sub-assets: ")
    # iterate through all sub assets
    for nif_asset in additional_assets:
        found = False
        for asset_path in glob.iglob(os.path.join(ASSET_PATH, "UIX", "**", nif_asset),
                                     recursive=True):
            found = True
            relative_asset_path = os.path.relpath(os.path.realpath(asset_path), ASSET_PATH)
            if relative_asset_path in tar_ball.getnames():
                break  # file already exists, skip
            sys.stdout.write("\033[K")
            sys.stdout.write(next(spinner))
            sys.stdout.write(" [{0}]".format(relative_asset_path))
            sys.stdout.flush()
            sys.stdout.write('\r\b')
            f.seek(0)   # reset to beginning of csv file
            for row in uixr_data:
                if row.get('asset').lower() == relative_asset_path.lower():
                    if row.get('license').lower() == 'cc0':
                        break  # good to go, break
                    else:
                        print("WARNING: Non-CC0 license asset -> {0}".format(relative_asset_path))
            tar_ball.add(asset_path, relative_asset_path)
        if not found:
            print("WARNING: sub-asset not found -> {0}".format(nif_asset))
    tar_ball.close()
