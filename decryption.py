import cv2
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to select an image
def select_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    return file_path

# Function to decrypt message from image
def decrypt():
    image_path = select_image()
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return
    
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Unable to load the image!")
        return
    
    password = password_entry.get()
    if not password:
        messagebox.showerror("Error", "Please enter a password!")
        return
    
    # Retrieve message length from the first pixel
    message_length = int(img[0, 0, 0])

    # ASCII Dictionary for Decoding
    c = {i: chr(i) for i in range(255)}

    message = ""
    n, m, z = 0, 0, 1  # Start at (0,0,1) to avoid length pixel
    for _ in range(message_length):
        message += c[int(img[n, m, z])]  # Fix KeyError issue
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    messagebox.showinfo("Decrypted Message", f"Hidden Message: {message}")

# GUI Layout
decrypt_root = tk.Tk()
decrypt_root.title("Image Steganography - Decryption")
decrypt_root.geometry("500x200")

tk.Label(decrypt_root, text="Enter Password:").pack()
password_entry = tk.Entry(decrypt_root, width=40, show="*")
password_entry.pack()

tk.Button(decrypt_root, text="Decrypt Image", command=decrypt).pack(pady=10)

decrypt_root.mainloop()
