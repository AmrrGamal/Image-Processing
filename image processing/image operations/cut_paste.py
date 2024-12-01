import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox 
import numpy as np
from PIL import Image


def cut_paste(image1, image2, cut_position=(0, 0), cut_size=(200, 200)): 
    if image1.mode != 'L':
        image1 = image1.convert('L')
    if image2.mode != 'L':
        image2 = image2.convert('L')

    if image1.size != image2.size:
        image2 = image2.resize(image1.size)

    img_array1 = np.array(image1, dtype=np.float32)
    img_array2 = np.array(image2, dtype=np.float32)

    height1, width1 = img_array1.shape[:2]  

    x, y = cut_position
    w, h = cut_size

    w = min(w, width1 - x)
    h = min(h, height1 - y)

    cut_image = img_array1[y:y + h, x:x + w]

    output_image = np.copy(img_array2)
    output_image[y:y + h, x:x + w] = cut_image

    output_image = np.clip(output_image, 0, 255)
    return Image.fromarray(output_image.astype(np.uint8))


def display_cut_paste_result(master, original_image_1, original_image_2):
    window = tk.Toplevel(master)
    window.title("Cut Paste Result")
    window.configure(bg="#f0f8ff")

    window_width = 1300
    window_height = 730

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = (screen_height // 2) - (window_height // 2)
    position_left = (screen_width // 2) - (window_width // 2)
    window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    cut_paste_image = cut_paste(original_image_1, original_image_2)

    original_image_1_resized = ImageTk.PhotoImage(original_image_1.resize((300, 300)))
    original_image_2_resized = ImageTk.PhotoImage(original_image_2.resize((300, 300)))
    cut_paste_image_resized = ImageTk.PhotoImage(cut_paste_image.resize((300, 300)))

    original_image_1_label = tk.Label(window, image=original_image_1_resized)
    original_image_1_label.image = original_image_1_resized
    original_image_1_label.grid(row=0, column=0, padx=60, pady=10)

    original_image_2_label = tk.Label(window, image=original_image_2_resized)
    original_image_2_label.image = original_image_2_resized
    original_image_2_label.grid(row=0, column=1, padx=60, pady=10)

    cut_paste_image_label = tk.Label(window, image=cut_paste_image_resized)
    cut_paste_image_label.image = cut_paste_image_resized
    cut_paste_image_label.grid(row=0, column=2, padx=60, pady=10)

    original_1_text = tk.Label(window, text="Original Image 1", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
    original_1_text.grid(row=1, column=0)

    original_2_text = tk.Label(window, text="Original Image 2", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
    original_2_text.grid(row=1, column=1)

    result_text = tk.Label(window, text="Cut Paste result", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
    result_text.grid(row=1, column=2)

