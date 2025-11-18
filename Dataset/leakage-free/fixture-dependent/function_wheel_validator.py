import os
from wheel.cli import WheelError
from wheel.wheelfile import WheelFile


class WheelValidator:
    def validate_wheel_file(self, wheel_path: str) -> dict:

        result = {
            'is_valid': False,
            'name': None,
            'version': None,
            'error_msg': None
        }

        if not os.path.exists(wheel_path):
            raise FileNotFoundError('Error: Wheel file does not exist')

        try:
            with WheelFile(wheel_path) as wf:

                result['name'] = wf.parsed_filename.group('name')
                result['version'] = wf.parsed_filename.group('ver')

                wf.verify()
                result['is_valid'] = True
        except WheelError as e:
            raise e
        except Exception as e:
            raise e

        return result