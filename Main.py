#rename images to png

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class ImageRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Renamer")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        self.folder_path = ""
        self.setup_ui()
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Folder selection section
        folder_frame = tk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(folder_frame, text="Image Folder:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.folder_entry = tk.Entry(folder_frame)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(folder_frame, text="Browse", command=self.browse_folder)
        browse_button.pack(side=tk.RIGHT)
        
        # Output name section
        name_frame = tk.Frame(main_frame)
        name_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(name_frame, text="Base Name:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.name_entry = tk.Entry(name_frame)
        self.name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.name_entry.insert(0, "image")
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = tk.Label(main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # Process button
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        process_button = tk.Button(button_frame, text="Rename Images", command=self.process_images, 
                                  bg="#4CAF50", fg="white", padx=20, pady=10)
        process_button.pack()
    
    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_path)
            self.status_var.set(f"Selected folder: {folder_path}")
    
    def process_images(self):
        folder_path = self.folder_entry.get()
        base_name = self.name_entry.get()
        
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder")
            return
        
        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Selected folder does not exist")
            return
        
        if not base_name:
            messagebox.showerror("Error", "Please enter a base name")
            return
        
        # Find all image files
        files = os.listdir(folder_path)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        image_files = [f for f in files if os.path.splitext(f.lower())[1] in image_extensions]
        
        if not image_files:
            messagebox.showinfo("Info", "No image files found in the selected folder")
            return
        
        # Sort files
        image_files.sort()
        
        # Process each image
        processed = 0
        errors = 0
        
        for i, filename in enumerate(image_files, 1):
            source_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"{base_name}{i}.png")
            
            try:
                # Update status
                self.status_var.set(f"Processing {i}/{len(image_files)}: {filename}")
                self.root.update()
                
                # Open and save image
                img = Image.open(source_path)
                img.save(output_path, "PNG")
                
                # Remove original file if different
                if source_path != output_path:
                    os.remove(source_path)
                
                processed += 1
            except Exception as e:
                errors += 1
                print(f"Error processing {filename}: {e}")
        
        # Show completion message
        if errors == 0:
            messagebox.showinfo("Success", f"Successfully renamed {processed} images!")
        else:
            messagebox.showwarning("Completed with errors", 
                                  f"Renamed {processed} images. {errors} files had errors.")
        
        self.status_var.set(f"Completed. Renamed {processed} images.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageRenamerApp(root)
    root.mainloop()