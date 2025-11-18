from __future__ import annotations
from pathlib import Path
import av

def convert_audio(input_path: Path, output_path: Path, codec_name: str):
    with av.open(input_path) as input_audio, av.open(output_path, 'w') as output_audio:
        input_audio_stream = input_audio.streams.audio[0]
        output_audio_stream = output_audio.add_stream(codec_name)
        for frame in input_audio.decode(input_audio_stream):
            for packet in output_audio_stream.encode(frame):
                output_audio.mux(packet)
        for packet in output_audio_stream.encode():
            output_audio.mux(packet)