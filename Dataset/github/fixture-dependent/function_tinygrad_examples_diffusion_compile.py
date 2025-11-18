import numpy as np

def convert_f32_to_f16(input_file, output_file):
    with open(input_file, 'rb') as f:
        metadata_length_bytes = f.read(8)
        metadata_length = int.from_bytes(metadata_length_bytes, byteorder='little', signed=False)
        metadata_json_bytes = f.read(metadata_length)
        float32_values = np.fromfile(f, dtype=np.float32)
    first_text_model_offset = 3772703308
    num_elements = int(first_text_model_offset / 4)
    front_float16_values = float32_values[:num_elements].astype(np.float16)
    rest_float32_values = float32_values[num_elements:]
    with open(output_file, 'wb') as f:
        f.write(metadata_length_bytes)
        f.write(metadata_json_bytes)
        front_float16_values.tofile(f)
        rest_float32_values.tofile(f)