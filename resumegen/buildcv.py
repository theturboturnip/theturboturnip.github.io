#!/usr/bin/env python3
# ^ requires python3.8+ for dataclasses

import argparse
import json
from dataclasses import dataclass
from typing import Dict, Any, Iterable, List, Optional, Union
import copy
import os
import tomllib

def read_toml(path: str) -> Dict[str, Any]:
    with open(path, "rb") as f:
        return tomllib.load(f)

def read_tomls(paths: Iterable[str]) -> Dict[str, Any]:
    config: Dict[str, Any] = {}
    for p in paths:
        extra_config = read_toml(p)
        merge_dicts(extra_config, config)
    if not config:
        raise RuntimeError("No tomls provided to read_tomls")
    return config

def merge_dicts(src: Dict[str, Any], dst: Dict[str, Any]):
    for k, v in src.items():
        if isinstance(v, dict):
            if k not in dst:
                dst[k] = {}
            merge_dicts(v, dst[k])
        else:
            dst[k] = v

def apply_config(src: Dict[str, Any], config: Dict[str, Union[Dict, List[str]]]):
    # Config = dict of key -> list of IDs
    # i.e. { "projects": ["warwick_typ"] }

    # Shallow copy - lists + objects within the data are shared
    # e.g. the "basics" object is the same in new_data and source_data - if you change x["basics"].phone, it changes in both
    dst = copy.copy(src)

    # For each thing the config changes
    # Create a new list for it in the dst, which holds references to objects in the src
    for k, vs in config.items():
        if isinstance(vs, dict):
            if isinstance(dst[k], dict):
                print(f"Updating fields of '{k}' - was already a dictionary")
                dst[k].update(vs)
            else:
                print(f"Setting field '{k}' to a dictionary - was {dst.get(k)} before")
                dst[k] = copy.copy(vs)
        elif isinstance(vs, list):
            src_id_dict = dict(src[k])

            try:
                dst[k] = [
                    src_id_dict[i]
                    for i in vs
                ]
            except KeyError as ex:
                ex.args = (f"no '{ex.args[0]}' in '{k}'",) + ex.args[1:]
                raise
        else:
            print(f"Assuming '{k}' is intended to directly override a field - it isn't a list or a dict!")
            dst[k] = vs
    return dst

def main() -> None:
    parser = argparse.ArgumentParser("buildcv")
    parser.add_argument("source_data", type=str, help="TOML file describing core resume content")
    parser.add_argument("configs", nargs='+', type=str, help="JSON file describing all resume configurations")
    parser.add_argument("--config", type=str, help="The single config to generate. Otherwise, all configs are generated")
    parser.add_argument("-o", type=str, default="./output/")

    args = parser.parse_args()

    source_data = read_toml(args.source_data)
    configs = read_tomls(args.configs)
    requested_config: Optional[str] = args.config

    if requested_config is None:
        configs_to_build = list(configs.keys())
    else:
        configs_to_build = [requested_config]

    for c_name in configs_to_build:
        c = configs[c_name]
        new_data = apply_config(source_data, c)
        with open(os.path.join(args.o, f"resume.{c_name}.json"), "w") as f:
            f.write(json.dumps(new_data, indent=4))
        

if __name__ == '__main__':
    main()
