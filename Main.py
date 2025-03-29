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