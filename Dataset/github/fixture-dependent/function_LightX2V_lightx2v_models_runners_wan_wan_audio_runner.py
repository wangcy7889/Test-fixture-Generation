import json
import os
from loguru import logger


def get_audio_files_from_audio_path(self, audio_path):
        if os.path.isdir(audio_path):
            audio_files = []
            mask_files = []
            logger.info(f"audio_path is a directory, loading config.json from {audio_path}")
            audio_config_path = os.path.join(audio_path, "config.json")
            assert os.path.exists(audio_config_path), "config.json not found in audio_path"
            with open(audio_config_path, "r") as f:
                audio_config = json.load(f)
            for talk_object in audio_config["talk_objects"]:
                audio_files.append(os.path.join(audio_path, talk_object["audio"]))
                mask_files.append(os.path.join(audio_path, talk_object["mask"]))
        else:
            logger.info(f"audio_path is a file without mask: {audio_path}")
            audio_files = [audio_path]
            mask_files = None

        return audio_files, mask_files
