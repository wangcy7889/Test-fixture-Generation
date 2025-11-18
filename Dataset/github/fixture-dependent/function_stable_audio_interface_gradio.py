import gc
import numpy as np
import torch
import torchaudio
from einops import rearrange
model = None
sample_rate = 32000

def autoencoder_process(audio, latent_noise, n_quantizers):
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    device = next(model.parameters()).device
    in_sr, audio = audio
    if audio.dtype == np.float32:
        audio = torch.from_numpy(audio)
    elif audio.dtype == np.int16:
        audio = torch.from_numpy(audio).float().div(32767)
    elif audio.dtype == np.int32:
        audio = torch.from_numpy(audio).float().div(2147483647)
    else:
        raise ValueError(f'Unsupported audio data type: {audio.dtype}')
    audio = audio.to(device)
    if audio.dim() == 1:
        audio = audio.unsqueeze(0)
    else:
        audio = audio.transpose(0, 1)
    audio = model.preprocess_audio_for_encoder(audio, in_sr)
    dtype = next(model.parameters()).dtype
    audio = audio.to(dtype)
    if n_quantizers > 0:
        latents = model.encode_audio(audio, chunked=False, n_quantizers=n_quantizers)
    else:
        latents = model.encode_audio(audio, chunked=False)
    if latent_noise > 0:
        latents = latents + torch.randn_like(latents) * latent_noise
    audio = model.decode_audio(latents, chunked=False)
    audio = rearrange(audio, 'b d n -> d (b n)')
    audio = audio.to(torch.float32).clamp(-1, 1).mul(32767).to(torch.int16).cpu()
    torchaudio.save('output.wav', audio, sample_rate)
    return 'output.wav'