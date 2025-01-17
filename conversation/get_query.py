import sounddevice as sd
import soundfile as sf
import argparse

# Default parameters
DEFAULT_DURATION = 5  # Default duration in seconds 默认录音时长（秒）

def main(duration):
    # File to store the recorded audio
    output_file = "recorded_audio.wav"  # 保存录音的文件路径

    # Device parameters
    record_device_id = 0  # Microphone device index (cv182xa_adc) 麦克风设备索引
    playback_device_id = 1  # Speaker device index (cv182xa_dac) 扬声器设备索引
    channels = [2]  # Use channel 2 of the microphone 使用麦克风的第2通道
    samplerate = 44100  # Sampling rate in Hz 采样率（Hz）

    try:
        # Step 1: Record audio
        print(f"Recording for {duration} seconds from device {record_device_id}, channel {channels}...")
        print(f"开始录音，从设备 {record_device_id} 的通道 {channels} 录制 {duration} 秒...")
        audio_data = sd.rec(frames=int(duration * samplerate), samplerate=samplerate, 
                            channels=len(channels), device=record_device_id, dtype='float32', mapping=channels)
        sd.wait()  # Wait until recording is finished 等待录音完成
        print("Recording finished.")
        print("录音完成。")

        # Save the recorded audio to a WAV file
        sf.write(output_file, audio_data, samplerate)  # 将录音数据保存到 WAV 文件
        print(f"Audio saved to {output_file}")
        print(f"音频已保存到文件 {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"发生错误：{e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Record and play back audio with adjustable duration. 录制并播放音频，可调节时长。"
    )
    # Add argument for duration 添加录音时长参数
    parser.add_argument(
        "--duration",
        type=int,
        default=DEFAULT_DURATION,
        help="Recording duration in seconds (default: 5). 录音时长（秒），默认值为 5。",
    )
    args = parser.parse_args()

    # Run the main function 运行主函数
    main(args.duration)