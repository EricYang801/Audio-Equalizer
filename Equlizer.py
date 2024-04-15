import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
from scipy.io.wavfile import write

import numpy as np

def apply_filter():
    global audio, filtered_audio

    # Get the frequency ranges from the scales
    low_freq_gain = int(low_scale.get())
    mid_low_freq_gain = int(mid_low_scale.get())
    mid_freq_gain = int(mid_scale.get())
    mid_high_freq_gain = int(mid_high_scale.get())
    high_freq_gain = int(high_scale.get())
    
    # 對每個頻率範圍應用濾波器
    low_pass = audio.low_pass_filter(100)
    low_pass = low_pass.apply_gain(low_freq_gain)
    mid_low_pass = audio.low_pass_filter(400).overlay(audio.high_pass_filter(100))
    mid_low_pass = mid_low_pass.apply_gain(mid_low_freq_gain)
    mid_pass = audio.low_pass_filter(1000).overlay(audio.high_pass_filter(400))
    mid_pass = mid_pass.apply_gain(mid_freq_gain)
    mid_high_pass = audio.low_pass_filter(2400).overlay(audio.high_pass_filter(1000))
    mid_high_pass = mid_high_pass.apply_gain(mid_high_freq_gain)
    high_pass = audio.high_pass_filter(15000)
    high_pass = high_pass.apply_gain(high_freq_gain)

    # 組合過濾後的片段
    filtered_audio = low_pass + mid_low_pass + mid_pass + mid_high_pass + high_pass

    # 確保 filtered_audio 的持續時間與原始音訊相匹配
    if len(filtered_audio) > len(audio):
        filtered_audio = filtered_audio[:len(audio)]
    elif len(filtered_audio) < len(audio):
        # 如果 filtered_audio 較短，則用靜音填充
        silence_duration = len(audio) - len(filtered_audio)
        silence = AudioSegment.silent(duration=silence_duration)
        filtered_audio += silence
    # 將處理後的音訊寫入檔案
    filtered_audio.export("processed_audio.mp3", format="mp3")
    root.destroy()  # 關閉 tkinter 窗口

def open_file():  # 定義一個函數來打開音訊檔案
    global audio  # 宣告 audio 為全域變數
    filepath = filedialog.askopenfilename()  # 打開檔案對話框並獲取檔案路徑
    audio = AudioSegment.from_file(filepath)  # 從檔案路徑讀取音訊

# 創建主窗口
root = tk.Tk()
root.title("Audio Equalizer")  # 設定窗口標題

# 為所有每個頻率範圍創建標籤和滑塊
low_label = tk.Label(root, text="Low Frequency Gain:")
low_label.pack()
low_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
low_scale.pack()

mid_low_label = tk.Label(root, text="Mid Low Frequency Gain:")
mid_low_label.pack()
mid_low_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
mid_low_scale.pack()

mid_label = tk.Label(root, text="Mid Frequency Gain:")
mid_label.pack()
mid_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
mid_scale.pack()

mid_high_label = tk.Label(root, text="Mid High Frequency Gain:")
mid_high_label.pack()
mid_high_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
mid_high_scale.pack()

high_label = tk.Label(root, text="High Frequency Gain:")
high_label.pack()
high_scale = tk.Scale(root, from_=-100, to=100, orient=tk.HORIZONTAL)
high_scale.pack()

# 創建按鈕來應用濾波器
apply_button = tk.Button(root, text="Apply Filter", command=apply_filter)
apply_button.pack()

# 創建按鈕來打開音訊檔案
open_button = tk.Button(root, text="Open Audio File", command=open_file)
open_button.pack()

# 運行 tkinter 事件循環
root.mainloop()