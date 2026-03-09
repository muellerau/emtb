#!/usr/bin/env python3

import pickle
import os
import sys

def dump_gridfs_file(file_path, output_dir="extracted_fsc"):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Unpacking {file_path} into {output_dir}...")

    with open(file_path, 'rb') as f:
        try:
            # CryoSPARC often uses pickle for these bundles
            gfs = pickle.load(f)
            
            # The structure is usually a dict where keys are filenames
            if isinstance(gfs, list):
                for x in gfs:
                    if not isinstance(x, dict):
                        print("Unexpected element, skipping...")
                        continue
                    out_path = os.path.join(output_dir, x['filename'])
                    with open(out_path, 'wb') as out_f:
                        out_f.write(x['data'])
                    print(f"  Extracted: {x['filename']}")
            else:
                print("Unexpected file format inside the bundle.")
        except Exception as e:
            print(f"Failed to unpack: {e}")

if __name__ == "__main__":
    # Usage: python script.py /path/to/gridfsdata_0
    path = sys.argv[1] if len(sys.argv) > 1 else 'gridfsdata_0'
    dump_gridfs_file(path)
