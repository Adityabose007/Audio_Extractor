import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from moviepy import VideoFileClip


class AudioExtractorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Audio Extractor")
        self.root.geometry("500x250")
        self.root.resizable(False, False)

        # Variables to store paths
        self.video_path = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # --- Video Selection Row ---
        tk.Label(self.root, text="Select Video:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, padx=10, pady=15, sticky="w"
        )
        tk.Entry(
            self.root, textvariable=self.video_path, width=40, state="readonly"
        ).grid(row=0, column=1, padx=5, pady=15)
        tk.Button(
            self.root, text="Browse", command=self.browse_video, width=10
        ).grid(row=0, column=2, padx=10, pady=15)

        # --- Output Folder Row ---
        tk.Label(
            self.root, text="Save Audio To:", font=("Arial", 10, "bold")
        ).grid(row=1, column=0, padx=10, pady=15, sticky="w")
        tk.Entry(
            self.root, textvariable=self.output_dir, width=40, state="readonly"
        ).grid(row=1, column=1, padx=5, pady=15)
        tk.Button(
            self.root, text="Browse", command=self.browse_output, width=10
        ).grid(row=1, column=2, padx=10, pady=15)

        # --- Progress Bar ---
        self.progress = ttk.Progressbar(
            self.root, orient="horizontal", length=460, mode="determinate"
        )
        self.progress.grid(row=2, column=0, columnspan=3, padx=20, pady=10)

        # --- Extract Button ---
        self.extract_btn = tk.Button(
            self.root,
            text="Extract Audio (MP3)",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.extract_audio,
            height=2,
            width=25,
        )
        self.extract_btn.grid(row=3, column=0, columnspan=3, pady=15)

    def browse_video(self):
        file_types = [
            (
                "Video Files",
                "*.3gpp *.mp4 *.mkv *.avi *.mov *.flv *.webm *.mpeg",
            ),
            ("All Files", "*.*"),
        ]
        selected_file = filedialog.askopenfilename(
            title="Select a Video File", filetypes=file_types
        )
        if selected_file:
            self.video_path.set(selected_file)
            # Auto-set the output directory to the same folder as the video
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(selected_file))

    def browse_output(self):
        selected_dir = filedialog.askdirectory(title="Select Output Folder")
        if selected_dir:
            self.output_dir.set(selected_dir)

    def extract_audio(self):
        video_file = self.video_path.get()
        output_folder = self.output_dir.get()

        # Validation checks
        if not video_file:
            messagebox.showerror("Error", "Please select a video file first!")
            return
        if not output_folder:
            messagebox.showerror(
                "Error", "Please select a destination folder!"
            )
            return

        try:
            # Disable button and start progress simulation
            self.extract_btn.config(state="disabled", text="Processing...")
            self.progress["value"] = 20
            self.root.update_idletasks()

            # Generate output filename dynamically based on input video name
            base_name = os.path.splitext(os.path.basename(video_file))[0]
            output_file_path = os.path.join(
                output_folder, f"{base_name}_Extracted.mp3"
            )

            self.progress["value"] = 40
            self.root.update_idletasks()

            # MoviePy core processing
            video_clip = VideoFileClip(video_file)
            audio_clip = video_clip.audio

            self.progress["value"] = 60
            self.root.update_idletasks()

            # Extracting audio (logger=None suppresses annoying terminal spam)
            audio_clip.write_audiofile(output_file_path, logger=None)

            self.progress["value"] = 90
            self.root.update_idletasks()

            # Resource Cleanup
            audio_clip.close()
            video_clip.close()

            # Completion state
            self.progress["value"] = 100
            messagebox.showinfo(
                "Success", f"Audio successfully saved to:\n{output_file_path}"
            )

        except Exception as e:
            messagebox.showerror(
                "Extraction Failed", f"An error occurred:\n{str(e)}"
            )

        finally:
            # Reset UI elements
            self.extract_btn.config(state="normal", text="Extract Audio (MP3)")
            self.progress["value"] = 0


if __name__ == "__main__":
    root = tk.Tk()
    app = AudioExtractorApp(root)
    root.mainloop()