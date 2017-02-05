#!/usr/bin/python
import csv
import os
import tarfile

RELEASE_PATH = "uixr-assets-cc0-1.0.tar.gz"

with open("Manifests/UIXR.manifest") as f:
    uixr_data = csv.DictReader(f)

    tar_ball = tarfile.open(RELEASE_PATH, "w:")

    for row in uixr_data:
        if row.get('license').upper() == 'CC0':
            tar_ball.add(os.path.join('../../../Private', row.get('asset')), row.get('asset'))

    tar_ball.close()
