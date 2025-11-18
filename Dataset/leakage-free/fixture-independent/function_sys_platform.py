import sys


def get_os_info():
    platform_info = sys.platform.lower()
    if platform_info.startswith('linux'):
        if 'ubuntu' in platform_info:
            return 'ubuntu'
        elif'redhat' in platform_info:
            return'redhat'
        else:
            return 'linux_other'
    elif platform_info.startswith('win'):
        if 'win32' in platform_info:
            return 'windows_32bit'
        elif 'win64' in platform_info:
            return 'windows_64bit'
        return 'windows_other'
    elif platform_info.startswith('darwin'):
        if'mojave' in platform_info:
            return'macos_mojave'
        elif 'catalina' in platform_info:
            return'macos_catalina'
        return'macos_other'
    return platform_info