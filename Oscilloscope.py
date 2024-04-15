# 引入所需的模組
import numpy as np  # 用於數學運算
import matplotlib.pyplot as plt  # 用於繪圖
from pydub import AudioSegment  # 用於處理音訊
import tkinter as tk  # 用於建立圖形使用者介面
from tkinter import filedialog  # 用於打開檔案對話框

# 定義繪製頻譜圖的函數
def plot_spectrogram():
    # 打開檔案對話框，讓使用者選擇音訊檔案
    file_path = filedialog.askopenfilename()
    # 如果使用者選擇了檔案
    if file_path:
        # 讀取音訊檔案
        audio = AudioSegment.from_file(file_path)

        # 將音訊轉換為numpy array
        audio_signal = np.array(audio.get_array_of_samples())
        # 獲取音訊的取樣率
        sampling_rate = audio.frame_rate

        # 定義不同頻率範圍
        low_freq_range = (100, 400)
        mid_low_freq_range = (400, 1000)
        mid_freq_range = (1000, 2400)
        mid_high_freq_range = (2400, 15000)
        high_freq_range = (15000, 20000)

        # 對音訊信號進行快速傅立葉變換(FFT)
        fft_result = np.fft.fft(audio_signal)
        # 計算FFT結果對應的頻率
        frequencies = np.fft.fftfreq(len(fft_result), 1 / sampling_rate)

        # 創建新的圖形窗口
        plt.figure()

        # 繪製FFT結果 (取對數使幅度更明顯)
        plt.plot(frequencies, 20 * np.log10(np.abs(fft_result)))

        # 繪製不同頻率範圍
        plt.axvspan(low_freq_range[0], low_freq_range[1], color='blue', alpha=0.3)
        plt.axvspan(mid_low_freq_range[0], mid_low_freq_range[1], color='green', alpha=0.3)
        plt.axvspan(mid_freq_range[0], mid_freq_range[1], color='yellow', alpha=0.3)
        plt.axvspan(mid_high_freq_range[0], mid_high_freq_range[1], color='orange', alpha=0.3)
        plt.axvspan(high_freq_range[0], high_freq_range[1], color='red', alpha=0.3)

        # 設定圖表標題和軸標籤
        plt.title('Audio Spectrogram')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (dB)')

        # 設定x軸和y軸的範圍
        plt.xlim(100, 20000)
        plt.ylim(40, 200)

        # 設定y軸的刻度
        plt.yticks(np.arange(40, 201, 20))

        # 顯示網格
        plt.grid(True)

        # 顯示圖表
        plt.show()

# 建立主視窗
root = tk.Tk()
root.title("Audio Spectrogram")

# 創建按鈕，點擊後會呼叫plot_spectrogram函數
button = tk.Button(root, text="Open Audio File", command=plot_spectrogram)
button.pack()

# 執行主迴圈，開始接收使用者事件
root.mainloop()