#!/usr/bin/env python3
import csv
import glob
from multiprocessing import Process, Queue, current_process
from nif_walker import walk_nif
import os
import sys
import tarfile

RELEASE_PATH = "uixr-assets-le-1.3.tar"
ASSET_PATH = "../../../Private"


def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


def get_filename(string):
    return os.path.basename(string.replace("\\", "/"))


def insensitive_glob(pattern, recursive):
    def either(c):
        return '[%s%s]' % (c.lower(), c.upper()) if c.isalpha() else c
    return glob.iglob(''.join(map(either, pattern)), recursive=recursive)


def find_match(ap, rap):
    asset_filename, asset_extension = os.path.splitext(ap.lower())
    relative_asset_filename, relative_asset_extension = os.path.splitext(rap.lower())

    if asset_filename == relative_asset_filename:
        return True
    else:
        return False


def retrieve_assets_from_nif(nif_path):
    # check that we have all related assets
    assets = []
    nif_assets = walk_nif(nif_path=nif_path, use_stdout=False)
    for asset_string in nif_assets:
        for asset_name in asset_string.split(', '):
            assets.append(get_filename(asset_name).lower())
    return assets


def worker(work_queue, done_queue):
    spinner = spinning_cursor()
    p = current_process()
    for nif_path in iter(work_queue.get, 'STOP'):
        sys.stdout.write("\r\b\033[K{0} [{1}][{2}][{3}]".format(
            next(spinner), work_queue.qsize(), p.name, nif_path))
        sys.stdout.flush()
        assets = []
        try:
            # assets.append('DEADBEEF')
            assets = retrieve_assets_from_nif(nif_path)
        except Exception:
            pass
        done_queue.put((nif_path, assets))
    done_queue.put('STOP')
    return True


def main():
    with open("Manifests/UIXR.manifest") as f:
        uixr_data = csv.DictReader(f)
        tar_ball = tarfile.open(RELEASE_PATH, "w:")
        spinner = spinning_cursor()
        manifest = []
        additional_assets = []
        additional_assets_nif = {}

        # setup multi-processing job
        workers = 8
        processes = []
        work_queue = Queue()
        done_queue = Queue()

        print("Gathering assets: ")
        for row in uixr_data:
            row_license = row.get('license').lower()
            if row_license == 'cc0' or row_license == 'cc-by' or row_license == 'cc-by-nc':
                sys.stdout.write("\r\b \033[K{0} [{1}]".format(next(spinner), row.get('asset')))
                sys.stdout.flush()
                file_path = os.path.join(ASSET_PATH, row.get('asset'))
                if not os.path.exists(file_path):
                    print("WARNING: asset not found -> {0}".format(row.get('asset')))
                    continue
                manifest.append(row.get('asset'))
                tar_ball.add(file_path, row.get('asset'))

                work_queue.put(file_path)

        # let multiprocessing parse the nifs
        print("\n\nParsing NIFs for additional sub-assets: ")
        for i in range(workers):
            p = Process(target=worker, args=(work_queue, done_queue))
            processes.append(p)
            work_queue.put('STOP')
            p.start()

        stops = 0
        while True:
            item = done_queue.get()
            if isinstance(item, str) and item == 'STOP':
                stops += 1
                if stops == workers:
                    break
            else:
                # for worker_name, nif_name, nif_assets in iter(done_queue.get, 'STOP'):
                nif_path, nif_assets = item
                additional_assets += nif_assets
                additional_assets_nif[nif_path] = nif_assets

        print("\n\nFiltering assets.")
        # remove duplicates
        additional_assets = set(additional_assets)

        # remove blank entry in set
        if '' in additional_assets:
            additional_assets.remove('')

        # remove files listed in manifest, we already have them
        for asset in manifest:
            filename = os.path.basename(asset).lower()
            if filename in additional_assets:
                additional_assets.remove(filename)

        # match assets back to NIF
        additional_assets = list(additional_assets)
        for i in range(len(additional_assets)):
            asset = additional_assets[i]
            nifs_found = []
            for nif, assets in additional_assets_nif.items():
                if asset in assets:
                    nifs_found.append(nif)
            additional_assets[i] = (asset, [nif.replace(ASSET_PATH, '') for nif in nifs_found])

        print("\n\nGathering sub-assets: ")
        # iterate through all sub assets
        for nif_asset, nifs in additional_assets:
            found = False
            na_filename, _ = os.path.splitext(nif_asset.lower())
            na_filename += '.*'
            glob_path = os.path.join(ASSET_PATH, "UIX", "**", na_filename)
            for asset_path in insensitive_glob(glob_path, True):
                found = True
                relative_asset_path = os.path.relpath(os.path.realpath(asset_path), ASSET_PATH)
                if relative_asset_path in tar_ball.getnames():
                    break  # file already exists, skip
                sys.stdout.write("\r\b\033[K{0} [{1}]".format(next(spinner), relative_asset_path))
                sys.stdout.flush()
                f.seek(0)   # reset to beginning of csv file
                for row in uixr_data:
                    if find_match(row.get('asset'), relative_asset_path):
                        row_license = row.get('license').lower()
                        if row_license == 'cc0':
                            break  # good to go, break
                        elif row_license == 'cc-by':
                            break  # good to go, break
                        elif row_license == 'cc-by-nc':
                            break  # good to go, break
                        elif row_license == 'cc-by-sa':
                            break  # good to go, break
                        else:
                            print("\nWARNING: Non-CC license asset -> {0} ({1})\n".format(
                                relative_asset_path, nifs))
            if not found:
                print("\nWARNING: sub-asset not found -> {0} ({1})\n".format(nif_asset, nifs))
        tar_ball.close()


if __name__ == "__main__":
    main()