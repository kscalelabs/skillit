import sounddevice as sd
import soundfile as sf
import argparse

# Default parameters
DEFAULT_DURATION = 5  # Default duration in seconds 默认录音时长（秒）

def main():
    # File to store the recorded audio
    output_file = "response.wav"  # 保存录音的文件路径

    # Device parameters
    record_device_id = 0  # Microphone device index (cv182xa_adc) 麦克风设备索引
    playback_device_id = 1  # Speaker device index (cv182xa_dac) 扬声器设备索引
    channels = [2]  # Use channel 2 of the microphone 使用麦克风的第2通道
    samplerate = 8000  # Sampling rate in Hz 采样率（Hz）

    try:
        # Step 2: Play back the recorded audio
        print(f"Playing back on device {playback_device_id}...")
        print(f"开始播放录音，通过设备 {playback_device_id} 播放...")
        data, samplerate = sf.read(output_file)  # Load the recorded file 加载录音文件
        sd.play(data, samplerate=samplerate, device=playback_device_id)  # Play the audio 播放音频
        sd.wait()  # Wait for playback to complete 等待播放完成
        print("Playback finished.")
        print("播放完成。")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"发生错误：{e}")

if __name__ == "__main__":
    main()