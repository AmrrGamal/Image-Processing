import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox 
import numpy as np
from PIL import Image

def prewit_operator(image):
    if image.mode != 'L':
        image = image.convert('L')

    img_array = np.array(image, dtype=np.float32)
    height, width = img_array.shape

    prewitt_x = np.array([[1, 0, -1],
                          [1, 0, -1],
                          [1, 0, -1]], dtype=np.float32)
    
    prewitt_y = np.array([[1, 1, 1],
                          [0, 0, 0],
                          [-1, -1, -1]], dtype=np.float32)
    
    grad_x = np.zeros_like(img_array)
    grad_y = np.zeros_like(img_array)
    
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            region = img_array[i-1:i+2, j-1:j+2]  
            grad_x[i, j] = np.sum(region * prewitt_x)
            grad_y[i, j] = np.sum(region * prewitt_y)
    
    result = np.sqrt(grad_x**2 + grad_y**2)
    result = np.clip(result, 0, 255)
    result_image = Image.fromarray(result.astype(np.uint8))

    return result_image

def display_prewit_result(master, original_image):
     if original_image:
        window = tk.Toplevel(master)
        window.title("Prewit Result")
        window.geometry("900x500")
        window.configure(bg="#f0f8ff")
        
        window_width = 900
        window_height = 500
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_top = (screen_height // 2) - (window_height // 2)
        position_left = (screen_width // 2) - (window_width // 2)
        window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        image = prewit_operator(original_image)

        if image:
            original_resized = ImageTk.PhotoImage(original_image.resize((400, 300)))
            resized = ImageTk.PhotoImage(image.resize((400, 300)))

            original_label = tk.Label(window, image=original_resized)
            original_label.image = original_resized
            original_label.grid(row=0, column=0, padx=20, pady=20)

            label = tk.Label(window, image=resized)
            label.image = resized
            label.grid(row=0, column=1, padx=20, pady=20)

            original_text = tk.Label(window, text="Original Image", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
            original_text.grid(row=1, column=0)

            text = tk.Label(window, text="Prewit Image", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
            text.grid(row=1, column=1)

            back_button = tk.Button(window, text="Back to Upload", command=window.destroy, bg="#4a90e2", fg="white", font=("Arial", 14))
            back_button.grid(row=2, column=0, columnspan=2, pady=20)

     else:
        messagebox.showerror("Error", "Please upload an image first.")


