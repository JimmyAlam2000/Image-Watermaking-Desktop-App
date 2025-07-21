import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Application")

        self.image_path = None
        self.watermarked_image = None

        # Upload image
        self.upload_btn = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10)

        # Watermark text entry
        self.text_label = tk.Label(root, text="Enter Watermark Text:")
        self.text_label.pack()
        self.text_entry = tk.Entry(root, width=40)
        self.text_entry.pack(pady=5)

        # Add watermark button
        self.add_text_btn = tk.Button(root, text="Add Watermark Text", command=self.add_watermark_text)
        self.add_text_btn.pack(pady=10)

        # Save button
        self.save_btn = tk.Button(root, text="Save Watermarked Image", command=self.save_image, state='disabled')
        self.save_btn.pack(pady=10)

        # Image display canvas
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()

    def upload_image(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        self.image_path = filedialog.askopenfilename(filetypes=filetypes)
        if self.image_path:
            self.display_image(self.image_path)

    def display_image(self, path):
        img = Image.open(path)
        img.thumbnail((500, 500))
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(250, 250, image=self.tk_img)

    def add_watermark_text(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Please upload an image first.")
            return

        text = self.text_entry.get()
        if not text:
            messagebox.showwarning("No text", "Please enter watermark text.")
            return

        img = Image.open(self.image_path).convert("RGBA")
        txt_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # You can change font path and size here
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        # Calculate text size using textbbox (new method in Pillow)
        bbox = draw.textbbox((0, 0), text, font=font)
        textwidth = bbox[2] - bbox[0]
        textheight = bbox[3] - bbox[1]

        width, height = img.size
        x = width - textwidth - 20
        y = height - textheight - 20

        draw.text((x, y), text, font=font, fill=(192, 192, 192, 255))

        watermarked = Image.alpha_composite(img, txt_layer)
        self.watermarked_image = watermarked.convert("RGB")

        # Show watermarked image
        temp_path = "temp_preview.jpg"
        self.watermarked_image.save(temp_path)
        self.display_image(temp_path)

        self.save_btn.config(state='normal')

    def save_image(self):
        if not self.watermarked_image:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                 filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        if save_path:
            self.watermarked_image.save(save_path)
            messagebox.showinfo("Success", f"Image saved to {save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
