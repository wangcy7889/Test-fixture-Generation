import glob
import os
import subprocess
import sys
from ansible.module_utils.common.text.converters import to_native, to_text

def ansiballz_setup(modfile, modname, interpreters):
    os.system('chmod +x %s' % modfile)
    if 'ansible_python_interpreter' in interpreters:
        command = [interpreters['ansible_python_interpreter']]
    else:
        command = []
    command.extend([modfile, 'explode'])
    cmd = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = cmd.communicate()
    out, err = (to_text(out, errors='surrogate_or_strict'), to_text(err))
    lines = out.splitlines()
    if len(lines) != 2 or 'Module expanded into' not in lines[0]:
        print('*' * 35)
        print('INVALID OUTPUT FROM ANSIBALLZ MODULE WRAPPER')
        print(out)
        sys.exit(err)
    debug_dir = lines[1].strip()
    core_dirs = glob.glob(os.path.join(debug_dir, 'ansible/modules'))
    collection_dirs = glob.glob(os.path.join(debug_dir, 'ansible_collections/*/*/plugins/modules'))
    for module_dir in core_dirs + collection_dirs:
        for dirname, directories, filenames in os.walk(module_dir):
            for filename in filenames:
                if filename == modname + '.py':
                    modfile = os.path.join(dirname, filename)
                    break
    argsfile = os.path.join(debug_dir, 'args')
    print('* ansiballz module detected; extracted module source to: %s' % debug_dir)
    return (modfile, argsfile)