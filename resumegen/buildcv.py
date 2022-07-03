#!/usr/bin/env python3.8

import argparse
import json
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
import copy
import os

def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.loads(f.read())

def apply_config(src: Dict[str, Any], config: Dict[str, List[str]]):
    # Config = dict of key -> list of IDs
    # i.e. { "projects": ["warwick_typ"] }

    # Shallow copy - lists + objects within the data are shared
    # e.g. the "basics" object is the same in new_data and source_data - if you change x["basics"].phone, it changes in both
    dst = copy.copy(src)

    # For each thing the config changes
    # Create a new list for it in the dst, which holds references to objects in the src
    for k, vs in config.items():
        src_id_dict = {
            x["id"]:x
            for x in src[k]
        }

        dst[k] = [
            src_id_dict[i]
            for i in vs
            if i in src_id_dict
        ]

    return dst

def main():
    parser = argparse.ArgumentParser("buildcv")
    parser.add_argument("source_data", type=str, help="JSON file describing core resume content")
    parser.add_argument("configs", type=str, help="JSON file describing all resume configurations")
    parser.add_argument("--config", type=str, help="The single config to generate. Otherwise, all configs are generated")
    parser.add_argument("-o", type=str, default="./output/")

    args = parser.parse_args()

    source_data = read_json(args.source_data)
    configs = read_json(args.configs)
    requested_config: Optional[str] = args.config

    if requested_config is None:
        configs_to_build = list(configs.keys())
    else:
        configs_to_build = [requested_spec]

    for c_name in configs_to_build:
        c = configs[c_name]
        new_data = apply_config(source_data, c)
        with open(os.path.join(args.o, f"resume.{c_name}.json"), "w") as f:
            f.write(json.dumps(new_data, indent=4))
        

if __name__ == '__main__':
    main()