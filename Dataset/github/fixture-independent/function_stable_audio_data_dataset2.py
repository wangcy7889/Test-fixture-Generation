import random
import torch

def remove_long_silence(audio, sample_rate, silence_threshold=[0.01, 0.5], max_silence_duration=0.25):
    silence_energy_threshold, silence_duration_threshold = silence_threshold
    max_silence_samples = int(max_silence_duration * sample_rate)
    tiny_silence_samples = int(silence_duration_threshold * sample_rate)
    audio = audio.flatten()
    silence_mask = torch.abs(audio) < silence_energy_threshold
    silence_mask_diff = torch.diff(silence_mask.int())
    silence_starts = torch.where(silence_mask_diff == 1)[0] + 1
    silence_ends = torch.where(silence_mask_diff == -1)[0] + 1
    if silence_mask[0]:
        silence_starts = torch.cat((torch.tensor([0], device=silence_starts.device), silence_starts))
    if silence_mask[-1]:
        silence_ends = torch.cat((silence_ends, torch.tensor([len(audio)], device=silence_ends.device)))
    processed_audio = []
    prev_end = 0
    for start, end in zip(silence_starts, silence_ends):
        processed_audio.append(audio[prev_end:start])
        silence_segment = audio[start:end]
        if len(silence_segment) > max_silence_samples:
            if len(silence_segment) > tiny_silence_samples:
                start_idx = random.randint(0, len(silence_segment) - tiny_silence_samples)
                processed_audio.append(silence_segment[start_idx:start_idx + tiny_silence_samples])
            else:
                processed_audio.append(silence_segment[:tiny_silence_samples])
        else:
            processed_audio.append(silence_segment)
        prev_end = end
    if prev_end < len(audio):
        processed_audio.append(audio[prev_end:])
    processed_audio_tensor = torch.cat(processed_audio).unsqueeze(0)
    return processed_audio_tensor