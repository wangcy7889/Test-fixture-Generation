import numpy as np
np.set_printoptions(suppress=True, linewidth=1000)
from tinygrad import Tensor, nn, Device

def fetch_weights() -> dict[str, Tensor]:
    m1 = Tensor.from_url('https://huggingface.co/allenai/OLMoE-1B-7B-0924/resolve/main/model-00001-of-00003.safetensors').to(Device.DEFAULT)
    m2 = Tensor.from_url('https://huggingface.co/allenai/OLMoE-1B-7B-0924/resolve/main/model-00002-of-00003.safetensors').to(Device.DEFAULT)
    m3 = Tensor.from_url('https://huggingface.co/allenai/OLMoE-1B-7B-0924/resolve/main/model-00003-of-00003.safetensors').to(Device.DEFAULT)
    return {**nn.state.safe_load(m1), **nn.state.safe_load(m2), **nn.state.safe_load(m3)}