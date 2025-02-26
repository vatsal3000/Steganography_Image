import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# Function to select an image
def select_image():
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    return file_path

# Function to encrypt message into image
def encrypt():
    image_path = select_image()
    if not image_path:
        messagebox.showerror("Error", "No image selected!")
        return
    
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Unable to load the image!")
        return
    
    msg = message_entry.get()
    password = password_entry.get()
    if not msg or not password:
        messagebox.showerror("Error", "Please enter a message and password!")
        return

    # ASCII Dictionary for Encoding
    d = {chr(i): i for i in range(255)}

    # Store message length in the first pixel
    img[0, 0, 0] = len(msg)

    # Encrypt message into image
    n, m, z = 0, 0, 1  # Start at (0,0,1) to avoid overwriting length
    for char in msg:
        img[n, m, z] = d[char]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3
    
    encrypted_image_path = os.path.join(os.path.dirname(image_path), "encryptedImage.png")
    cv2.imwrite(encrypted_image_path, img)
    messagebox.showinfo("Success", f"Encrypted image saved as: {encrypted_image_path}")

# GUI Layout
encrypt_root = tk.Tk()
encrypt_root.title("Image Steganography - Encryption")
encrypt_root.geometry("500x300")

tk.Label(encrypt_root, text="Enter Secret Message:").pack()
message_entry = tk.Entry(encrypt_root, width=40)
message_entry.pack()

tk.Label(encrypt_root, text="Enter Password:").pack()
password_entry = tk.Entry(encrypt_root, width=40, show="*")
password_entry.pack()

tk.Button(encrypt_root, text="Encrypt Image", command=encrypt).pack(pady=10)

encrypt_root.mainloop()
