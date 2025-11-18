from __future__ import annotations
from pathlib import Path
from ansible.parsing.utils.jsonify import jsonify
from ansible.parsing.splitter import parse_kv

def write_argsfile(argstring, json=False):
    argspath = Path('~/.ansible_test_module_arguments').expanduser()
    if json:
        args = parse_kv(argstring)
        argstring = jsonify(args)
    argspath.write_text(argstring)
    return argspath