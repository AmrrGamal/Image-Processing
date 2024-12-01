
import numpy as np
from PIL import Image
from histogram import calculate_histogram
import tkinter as tk
from PIL import ImageTk
from tkinter import messagebox 
import numpy as np
from PIL import Image

"""
Step-by-step  of the function histogram_peak_threshold_segmentation:

Step 1: Convert the image to grayscale if it is not already in 'L' mode (grayscale).
This ensures that the image is in a single-channel format, suitable for histogram-based processing.
"""

"""
Step 2: Convert the image to a numpy array with uint8 data type.
This allows easy manipulation of pixel values for thresholding and segmentation.
"""

"""
Step 3: Calculate the histogram of the image and the bin edges.
The histogram will help us understand the distribution of pixel intensity values in the image.
"""

"""
Step 4: Identify the peaks in the histogram and sort them.
Peaks in the histogram indicate significant intensity values that can be used to define thresholds.
"""

"""
Step 5: Determine the threshold values based on the number of peaks.
If fewer than two peaks are found, default thresholds (0 and 255) are used for full image segmentation.
Otherwise, calculate the thresholds from the peaks.
"""

"""
Step 6: Create a blank segmented image with the same size as the original image.
This image will hold the segmented result, with white pixels representing the segmented regions.
"""

"""
Step 7: Apply the thresholds to the image.
Pixels within the threshold range will be set to 255 (white), while others will remain 0 (black).
"""

"""
Step 8: Return the segmented image as a PIL Image.
The final segmented image is converted back to a PIL image format to be used or saved.
"""


def histogram_peak_threshold_segmentation(image):
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image, dtype=np.uint8)

    hist, bins = calculate_histogram(image) 
    peaks_indices = find_peaks_and_sort_them(hist)

    if len(peaks_indices) < 2:
        print("Not enough peaks found. Defaulting to full image thresholding.")
        low_threshold, high_threshold = 0, 255 
    else:
        low_threshold, high_threshold = calculate_low_and_high_thresholds(peaks_indices)

    segmented_image = np.zeros_like(img_array)
    segmented_image[(img_array >= low_threshold) & (img_array <= high_threshold)] = 255

    return Image.fromarray(segmented_image)


def find_peaks_and_sort_them(hist):
    peaks = find_peaks_from_histogram(hist, height=0)
    if not peaks:
        return []
    
    sorted_peaks = sorted(peaks, key=lambda x: hist[x], reverse=True)
    return sorted_peaks[:2] if len(sorted_peaks) >= 2 else sorted_peaks


def calculate_low_and_high_thresholds(peaks_indices):
    peak1 = peaks_indices[0]
    peak2 = peaks_indices[1]

    low_threshold = (peak1 + peak2) // 2
    high_threshold = peak2

    return low_threshold, high_threshold


def find_peaks_from_histogram(hist, height=0):
    peaks = []
    hist = np.array(hist)
    for i in range(1, len(hist) - 1):
        if hist[i] > hist[i - 1] and hist[i] > hist[i + 1]:
            if hist[i] >= height:
                peaks.append(i) 
    
    if hist[0] > hist[1] and hist[0] >= height:
        peaks.insert(0, 0)  
    if hist[-1] > hist[-2] and hist[-1] >= height:
        peaks.append(len(hist) - 1)  

    return peaks




def display_peak_segmetation_result(master, original_image):
    if original_image:
        window = tk.Toplevel(master)
        window.title("Peak Segmetation Result")
       
        window.configure(bg="#f0f8ff")
        
        window_width = 900
        window_height = 500
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        position_top = (screen_height // 2) - (window_height // 2)
        position_left = (screen_width // 2) - (window_width // 2)
        
        window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

        peak_seg_image = histogram_peak_threshold_segmentation(original_image)

        if peak_seg_image:
            original_resized = ImageTk.PhotoImage(original_image.resize((400, 300)))
            peak_seg_resized = ImageTk.PhotoImage(peak_seg_image.resize((400, 300)))

            original_label = tk.Label(window, image=original_resized)
            original_label.image = original_resized
            original_label.grid(row=0, column=0, padx=20, pady=20)

            label = tk.Label(window, image=peak_seg_resized)
            label.image = peak_seg_resized
            label.grid(row=0, column=1, padx=20, pady=20)

            original_text = tk.Label(window, text="Original Image", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
            original_text.grid(row=1, column=0)

            text = tk.Label(window, text="Peak Segmented Image", font=("Arial", 14, "bold"), fg="#4a90e2", bg="#f0f8ff")
            text.grid(row=1, column=1)

            back_button = tk.Button(window, text="Back to Upload", command=window.destroy, bg="#4a90e2", fg="white", font=("Arial", 14))
            back_button.grid(row=2, column=0, columnspan=2, pady=20)

    else:
        messagebox.showerror("Error", "Please upload an image first.")

