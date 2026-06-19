#!/usr/bin/env python3
"""
dialogue_alan_xiaoj.py - Alan 與 小J 的語音對話生成。
自動偵測裝置並使用 CPU 推理，模型只載入一次，逐句生成最後拼接。
"""
from voxcpm import VoxCPM
import soundfile as sf
import numpy as np
import time
import os

REPO_DIR = os.path.dirname(os.path.abspath(__file__))

# 對話腳本
dialogue = [
    ("Alan", "嗨小J，聽說你最近克隆的聲音很受歡迎耶，是不是偷偷去上美聲課啊？"),
    ("小J", "哪有啦，明明就是天生麗質！倒是你Alan，怎麼聽起來有點宅男的感覺呀？"),
    ("Alan", "哈哈，那是資深工程師的知性美！你那台灣腔才可愛，聽了都快融化了。"),
    ("小J", "哎呦，算你會說話！那下次請我喝飲料，我就原諒你囉！"),
    ("Alan", "沒問題，一杯珍奶換你的可愛女聲，成交！")
]

def detect_device():
    gpu_type_file = os.path.join(REPO_DIR, '.gpu_type')
    if os.path.exists(gpu_type_file):
        with open(gpu_type_file, 'r', encoding='utf-8') as f:
            gpu_type = f.read().strip()
    else:
        import torch
        if torch.cuda.is_available():
            gpu_type = 'cuda'
        elif hasattr(torch, 'xpu') and torch.xpu.is_available():
            gpu_type = 'xpu'
        else:
            gpu_type = 'cpu'
    device_map = {'cuda': 'cuda', 'xpu': 'xpu', 'cpu': 'cpu'}
    return device_map.get(gpu_type, 'cpu')

def load_voice(voice_name):
    voice_dir = os.path.join(REPO_DIR, "voices", voice_name)
    ref_wav = os.path.join(voice_dir, "ref_voice.wav")
    prompt_file = os.path.join(voice_dir, "prompt.txt")
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()
    return ref_wav, prompt_text

def main():
    device = detect_device()
    print(f"偵測到裝置: {device}")
    
    print("載入 VoxCPM2 模型...")
    t0 = time.time()
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, device=device, optimize=False)
    print(f"模型載入完成，耗時 {time.time()-t0:.1f}s\n")

    # 預載聲音參考資料
    voices = {}
    for name in ["Alan", "小J"]:
        voices[name] = load_voice(name)
        print(f"  已載入聲音: {name}")

    print(f"\n開始生成對話（{len(dialogue)} 句）...\n")

    clips = []
    for i, (speaker, text) in enumerate(dialogue, 1):
        ref_wav, prompt_text = voices[speaker]
        print(f"[{i}/{len(dialogue)}] {speaker}: {text}")

        t1 = time.time()
        wav = model.generate(
            text=text,
            prompt_wav_path=ref_wav,
            prompt_text=prompt_text,
            reference_wav_path=ref_wav,
            cfg_value=1.5,
            inference_timesteps=10,
        )
        elapsed = time.time() - t1
        duration = len(wav) / model.tts_model.sample_rate
        print(f"        -> 生成時長: {duration:.1f}s (耗時 {elapsed:.1f}s, RTF={elapsed/duration:.1f})")

        # 句子之間加 0.5 秒停頓
        pause = np.zeros(int(0.5 * model.tts_model.sample_rate), dtype=wav.dtype)
        clips.append(wav)
        clips.append(pause)

    # 拼接所有片段
    full_audio = np.concatenate(clips)
    total_duration = len(full_audio) / model.tts_model.sample_rate
    output_path = os.path.join(REPO_DIR, "output", "dialogue_alan_xiaoj.wav")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, full_audio, model.tts_model.sample_rate)

    print(f"\n對話生成完成！")
    print(f"  總長度: {total_duration:.1f}s")
    print(f"  存檔路徑: {output_path}")

if __name__ == "__main__":
    main()
