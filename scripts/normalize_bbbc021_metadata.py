#!/usr/bin/env python3

import argparse
import os.path
import re

import pandas as pd

parser = argparse.ArgumentParser(description='Convert BBBC021 metadata')
parser.add_argument('input_path', help='The path to the BBBC021 metadata file')
options = parser.parse_args()

assert os.path.exists(options.input_path)

bbbc021 = pd.read_csv(options.input_path)
normalized = pd.DataFrame(columns=[
    'Metadata_Plate', 'Metadata_Well', 'Metadata_Site', 'Plate_Map_Name',
    'DNA', 'Tubulin', 'Actin', 'Replicate', 'Compound_Concentration'
])


def join(path_series, filename_series):
    return path_series + os.sep + filename_series


normalized.Metadata_Plate = bbbc021.Image_Metadata_Plate_DAPI
normalized.Metadata_Well = bbbc021.Image_Metadata_Well_DAPI
normalized.DNA = join(bbbc021.Image_Metadata_Plate_DAPI,
                      bbbc021.Image_FileName_DAPI)
normalized.Tubulin = join(bbbc021.Image_Metadata_Plate_DAPI,
                          bbbc021.Image_FileName_Tubulin)
normalized.Actin = join(bbbc021.Image_Metadata_Plate_DAPI,
                        bbbc021.Image_FileName_Actin)
normalized.Replicate = bbbc021.Replicate
normalized.Metadata_Site = bbbc021.Image_FileName_DAPI.apply(
    lambda name: re.search(r'_(s\d+)_', name).group(1))
normalized.Compound_Concentration = (
    bbbc021.Image_Metadata_Compound + '_' +
    bbbc021.Image_Metadata_Concentration.apply(str))

print(normalized.to_csv(sep=',', index=False))
