import torch
import torchaudio
AUDIO_KEYS = ('flac', 'wav', 'mp3', 'm4a', 'ogg', 'opus')

def is_silence_audio(audio, silence_threshold=0.01, max_silence_ratio=0.3):
    silence_frames = torch.sum(audio.abs() < silence_threshold, dim=1)
    total_frames = audio.size(1)
    silence_ratio_per_channel = silence_frames / total_frames
    if torch.any(silence_ratio_per_channel > max_silence_ratio).item():
        output_path = f'rejected_audios/rejected_{silence_ratio_per_channel.item()}.wav'
        torchaudio.save(output_path, audio, 16000)
        print(f'Rejected: {silence_ratio_per_channel}')
    return torch.any(silence_ratio_per_channel > max_silence_ratio).item()