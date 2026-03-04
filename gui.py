import os
import sys
import threading
from PIL import Image

import customtkinter as ctk
from tkinter import filedialog, messagebox

# ── Must be set BEFORE importing paddle ──────────────────────────────────────
os.environ["FLAGS_use_mkldnn"] = "0"
os.environ["FLAGS_enable_pir_in_executor"] = "0"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocessing import preprocess_image, preprocess_numpy_image, pdf_to_images

# ── Theme ─────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT       = "#4F8EF7"
ACCENT_HOVER = "#3A7BE0"
BG_DARK      = "#0F1117"
BG_CARD      = "#1A1D27"
BG_PANEL     = "#141720"
TEXT_PRIMARY = "#F0F2FF"
TEXT_MUTED   = "#6B7280"
SUCCESS      = "#22D3A5"
BORDER       = "#2A2D3E"
WARN         = "#F59E0B"


class OCRApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("OCR Studio")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.configure(fg_color=BG_DARK)

        self.file_path       = None
        self.pdf_pages       = []
        self.current_page    = 0
        self.processed_imgs  = []
        self.extracted_texts = []

        # ── FIX: keep a strong reference so CTkImage is never GC'd ──────────
        self._ctk_image_ref  = None

        self._build_ui()

    # ─────────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=310, fg_color=BG_CARD, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(9, weight=1)

        # Logo
        lf = ctk.CTkFrame(sb, fg_color="transparent")
        lf.grid(row=0, column=0, padx=24, pady=(28, 2), sticky="w")
        ctk.CTkLabel(lf, text="●", font=("Georgia", 22),
                     text_color=ACCENT).grid(row=0, column=0, padx=(0, 8))
        ctk.CTkLabel(lf, text="OCR Studio", font=("Georgia", 22, "bold"),
                     text_color=TEXT_PRIMARY).grid(row=0, column=1)

        ctk.CTkLabel(sb, text="Optical Character Recognition",
                     font=("Helvetica", 11), text_color=TEXT_MUTED).grid(
            row=1, column=0, padx=24, pady=(0, 20), sticky="w")

        _sep(sb, row=2)
        _section_label(sb, "INPUT FILE", row=3)

        ctk.CTkButton(sb, text="  Upload Image / PDF", height=48,
                      font=("Helvetica", 13, "bold"),
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      corner_radius=12,
                      command=self._upload_file).grid(
            row=4, column=0, padx=20, pady=(4, 8), sticky="ew")

        self.file_label = ctk.CTkLabel(sb, text="No file selected",
                                       font=("Helvetica", 11),
                                       text_color=TEXT_MUTED, wraplength=255)
        self.file_label.grid(row=5, column=0, padx=24, pady=(0, 12), sticky="w")

        _sep(sb, row=6)
        _section_label(sb, "SETTINGS", row=7)

        sf = ctk.CTkFrame(sb, fg_color="transparent")
        sf.grid(row=8, column=0, padx=20, pady=4, sticky="new")
        sf.grid_columnconfigure(0, weight=1)

        # ── Engine dropdown ───────────────────────────────────────────────────
        _mini_label(sf, "OCR Engine", row=0)
        self.engine_var = ctk.StringVar(value="Tesseract")
        ctk.CTkOptionMenu(
            sf, values=["Tesseract", "PaddleOCR"],
            variable=self.engine_var,
            font=("Helvetica", 12),
            fg_color=BG_PANEL, button_color=WARN,
            button_hover_color="#D97706",
            dropdown_fg_color=BG_PANEL,
            corner_radius=10, height=40,
            command=self._on_engine_change).grid(
            row=1, column=0, pady=(4, 6), sticky="ew")

        self.engine_info = ctk.CTkLabel(
            sf, text="🔧  pytesseract  |  multi-language",
            font=("Helvetica", 10), text_color=TEXT_MUTED)
        self.engine_info.grid(row=2, column=0, pady=(0, 12), sticky="w")

        # ── Language ──────────────────────────────────────────────────────────
        self.lang_frame = ctk.CTkFrame(sf, fg_color="transparent")
        self.lang_frame.grid(row=3, column=0, sticky="ew")
        self.lang_frame.grid_columnconfigure(0, weight=1)

        _mini_label(self.lang_frame, "OCR Language", row=0)
        self.lang_var = ctk.StringVar(value="English")
        ctk.CTkOptionMenu(
            self.lang_frame,
            values=["English", "Arabic", "English + Arabic"],
            variable=self.lang_var,
            font=("Helvetica", 12),
            fg_color=BG_PANEL, button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=BG_PANEL,
            corner_radius=10, height=40).grid(
            row=1, column=0, pady=(4, 14), sticky="ew")

        # ── PDF DPI ───────────────────────────────────────────────────────────
        _mini_label(sf, "PDF Resolution (DPI)", row=4)
        self.dpi_var = ctk.StringVar(value="300")
        ctk.CTkOptionMenu(
            sf, values=["150", "200", "300", "400"],
            variable=self.dpi_var,
            font=("Helvetica", 12),
            fg_color=BG_PANEL, button_color=ACCENT,
            button_hover_color=ACCENT_HOVER,
            dropdown_fg_color=BG_PANEL,
            corner_radius=10, height=40).grid(
            row=5, column=0, pady=(4, 14), sticky="ew")

        self.save_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(sf, text="Save preprocessed image",
                        variable=self.save_var,
                        font=("Helvetica", 12), text_color=TEXT_PRIMARY,
                        fg_color=ACCENT, hover_color=ACCENT_HOVER,
                        corner_radius=6).grid(row=6, column=0,
                                              pady=(0, 8), sticky="w")

        _sep(sb, row=9)

        self.run_btn = ctk.CTkButton(
            sb, text="  Run OCR ▶", height=52,
            font=("Helvetica", 14, "bold"),
            fg_color=SUCCESS, hover_color="#18B88E",
            text_color="#001a12", corner_radius=14,
            command=self._run_ocr)
        self.run_btn.grid(row=10, column=0, padx=20, pady=20, sticky="ew")

        self.status_label = ctk.CTkLabel(sb, text="Ready",
                                         font=("Helvetica", 11),
                                         text_color=TEXT_MUTED)
        self.status_label.grid(row=11, column=0, padx=24,
                               pady=(0, 24), sticky="w")

    # ── Main panel ────────────────────────────────────────────────────────────
    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color=BG_PANEL, corner_radius=0)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(1, weight=1)

        # Top bar
        topbar = ctk.CTkFrame(main, fg_color=BG_CARD, height=56, corner_radius=0)
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        topbar.grid_columnconfigure(1, weight=1)
        topbar.grid_propagate(False)

        ctk.CTkLabel(topbar, text="Preview & Results",
                     font=("Georgia", 15, "bold"),
                     text_color=TEXT_PRIMARY).grid(
            row=0, column=0, padx=24, pady=16, sticky="w")

        # PDF page nav
        self.nav_frame = ctk.CTkFrame(topbar, fg_color="transparent")
        self.nav_frame.grid(row=0, column=1, padx=24, sticky="e")

        ctk.CTkButton(self.nav_frame, text="◀", width=36, height=32,
                      fg_color=BG_PANEL, hover_color=ACCENT,
                      corner_radius=8,
                      command=self._prev_page).grid(row=0, column=0, padx=4)

        self.page_label = ctk.CTkLabel(self.nav_frame, text="",
                                       font=("Helvetica", 12),
                                       text_color=TEXT_MUTED, width=90)
        self.page_label.grid(row=0, column=1, padx=4)

        ctk.CTkButton(self.nav_frame, text="▶", width=36, height=32,
                      fg_color=BG_PANEL, hover_color=ACCENT,
                      corner_radius=8,
                      command=self._next_page).grid(row=0, column=2, padx=4)

        self.nav_frame.grid_remove()

        # Left — image preview
        left = ctk.CTkFrame(main, fg_color=BG_DARK, corner_radius=16)
        left.grid(row=1, column=0, padx=(16, 8), pady=16, sticky="nsew")
        left.grid_rowconfigure(1, weight=1)
        left.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="PREPROCESSED IMAGE",
                     font=("Helvetica", 10, "bold"),
                     text_color=TEXT_MUTED).grid(
            row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        self.img_scroll = ctk.CTkScrollableFrame(
            left, fg_color="transparent",
            scrollbar_button_color=ACCENT)
        self.img_scroll.grid(row=1, column=0, padx=8, pady=(0, 8), sticky="nsew")
        self.img_scroll.grid_columnconfigure(0, weight=1)

        self.img_label = ctk.CTkLabel(
            self.img_scroll,
            text="Upload a file and run OCR\nto see the preview here",
            font=("Helvetica", 13), text_color=TEXT_MUTED)
        self.img_label.grid(row=0, column=0, pady=20)

        # Right — text output
        right = ctk.CTkFrame(main, fg_color=BG_DARK, corner_radius=16)
        right.grid(row=1, column=1, padx=(8, 16), pady=16, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        rt = ctk.CTkFrame(right, fg_color="transparent")
        rt.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        rt.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(rt, text="EXTRACTED TEXT",
                     font=("Helvetica", 10, "bold"),
                     text_color=TEXT_MUTED).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(rt, text="Copy", width=60, height=28,
                      font=("Helvetica", 11),
                      fg_color=BG_PANEL, hover_color=ACCENT,
                      corner_radius=8,
                      command=self._copy_text).grid(row=0, column=1, sticky="e")

        ctk.CTkButton(rt, text="Save .txt", width=70, height=28,
                      font=("Helvetica", 11),
                      fg_color=BG_PANEL, hover_color=ACCENT,
                      corner_radius=8,
                      command=self._save_text).grid(
            row=0, column=2, padx=(6, 0), sticky="e")

        self.text_box = ctk.CTkTextbox(
            right, font=("Courier New", 13),
            fg_color=BG_CARD, text_color=TEXT_PRIMARY,
            border_color=BORDER, border_width=1,
            corner_radius=12, wrap="word",
            scrollbar_button_color=ACCENT)
        self.text_box.grid(row=1, column=0, padx=16,
                           pady=(0, 16), sticky="nsew")

        self.progress = ctk.CTkProgressBar(
            main, fg_color=BG_CARD, progress_color=ACCENT,
            height=4, corner_radius=0)
        self.progress.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.progress.set(0)

    # ── Handlers ──────────────────────────────────────────────────────────────
    def _on_engine_change(self, choice):
        if choice == "PaddleOCR":
            self.engine_info.configure(text="🚀  PaddleOCR")
        else:
            self.engine_info.configure(text="🔧  pytesseract")

    def _upload_file(self):
        path = filedialog.askopenfilename(
            title="Select Image or PDF",
            filetypes=[
                ("Supported files", "*.png *.jpg *.jpeg *.bmp *.tiff *.pdf"),
                ("Images", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PDF", "*.pdf")])
        if not path:
            return
        self.file_path = path
        self.file_label.configure(text=os.path.basename(path),
                                  text_color=TEXT_PRIMARY)
        self.status_label.configure(text="File loaded ✓", text_color=SUCCESS)
        self.pdf_pages.clear()
        self.processed_imgs.clear()
        self.extracted_texts.clear()
        self.current_page = 0
        self.text_box.delete("1.0", "end")
        # Full reset: destroy old label (kills the stale pyimage reference)
        # and create a fresh one — this is the only reliable fix for
        # "pyimage10 doesn't exist" on the second+ file load.
        self._ctk_image_ref = None
        self.img_label.destroy()
        self.img_label = ctk.CTkLabel(
            self.img_scroll,
            text="File loaded — press  Run OCR ▶",
            font=("Helvetica", 13), text_color=TEXT_MUTED)
        self.img_label.grid(row=0, column=0, pady=20)
        self.nav_frame.grid_remove()

    def _lang_code(self):
        return {"English": "eng", "Arabic": "ara",
                "English + Arabic": "eng+ara"}.get(self.lang_var.get(), "eng")

    def _run_ocr(self):
        if not self.file_path:
            messagebox.showwarning("No file", "Please upload a file first.")
            return
        self.run_btn.configure(state="disabled", text="Processing…")
        self.progress.set(0)
        self._set_status("Starting…")
        threading.Thread(target=self._ocr_worker, daemon=True).start()

    def _ocr_worker(self):
        try:
            engine  = self.engine_var.get()
            lang    = self._lang_code()
            ext     = os.path.splitext(self.file_path)[1].lower()
            out_dir = "Output"
            os.makedirs(out_dir, exist_ok=True)

            # Lazy import keeps Paddle env vars effective
            if engine == "Tesseract":
                from tesseract_ocr import run_ocr
            else:
                from paddle_ocr import run_ocr

            # ── PDF ──────────────────────────────────────────────────────────
            if ext == ".pdf":
                self._set_status("Converting PDF pages…")
                self.pdf_pages = pdf_to_images(self.file_path)
                total = len(self.pdf_pages)
                self.processed_imgs.clear()
                self.extracted_texts.clear()

                for i, page_img in enumerate(self.pdf_pages):
                    self._set_status(f"Processing page {i+1}/{total}…",
                                     progress=i / total)
                    proc = preprocess_numpy_image(
                        page_img,
                        save_output=self.save_var.get(),
                        output_folder=out_dir,
                        save_name=f"preprocessed_page{i+1}.png")
                    self.processed_imgs.append(proc)
                    text = run_ocr(proc, language=lang)
                    self.extracted_texts.append(text)

                self.after(0, self._show_pdf_result)

            # ── Image ────────────────────────────────────────────────────────
            else:
                self._set_status("Preprocessing…", progress=0.3)
                proc = preprocess_image(self.file_path,
                                        save_output=self.save_var.get(),
                                        output_folder=out_dir)
                self.processed_imgs = [proc]

                self._set_status("Running OCR…", progress=0.6)
                text = run_ocr(proc, language=lang)
                self.extracted_texts = [text]

                self.after(0, self._show_image_result)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", str(e)))
            self.after(0, self._reset_btn)

    def _show_image_result(self):
        self.progress.set(1.0)
        self._display_image(self.processed_imgs[0])
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", self.extracted_texts[0])
        self.status_label.configure(text="Done ✓", text_color=SUCCESS)
        self._reset_btn()

    def _show_pdf_result(self):
        self.progress.set(1.0)
        self.current_page = 0
        self.nav_frame.grid()
        self._refresh_page()
        self.status_label.configure(text="Done ✓", text_color=SUCCESS)
        self._reset_btn()

    def _refresh_page(self):
        total = len(self.processed_imgs)
        self.page_label.configure(
            text=f"Page {self.current_page + 1} / {total}")
        self._display_image(self.processed_imgs[self.current_page])
        self.text_box.delete("1.0", "end")
        self.text_box.insert("1.0", self.extracted_texts[self.current_page])

    def _prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._refresh_page()

    def _next_page(self):
        if self.current_page < len(self.processed_imgs) - 1:
            self.current_page += 1
            self._refresh_page()

    def _display_image(self, numpy_img):
        """
        FIX for pyimage1 doesn't exist:
        - Always called from main thread via self.after()
        - Convert numpy -> PIL -> CTkImage all on main thread
        - Store strong ref on self so GC never collects it
        """
        pil_img = Image.fromarray(numpy_img).convert("RGB")
        pil_img.thumbnail((480, 700), Image.LANCZOS)

        # Build CTkImage on main thread (critical — Tk is not thread-safe)
        new_img = ctk.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=pil_img.size)

        # Strong ref prevents garbage collection
        self._ctk_image_ref = new_img

        self.img_label.configure(image=self._ctk_image_ref, text="")

    # ── Utilities ─────────────────────────────────────────────────────────────
    def _set_status(self, msg, progress=None):
        def _u():
            self.status_label.configure(text=msg, text_color=ACCENT)
            if progress is not None:
                self.progress.set(progress)
        self.after(0, _u)

    def _copy_text(self):
        text = self.text_box.get("1.0", "end").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_label.configure(text="Copied ✓", text_color=SUCCESS)

    def _save_text(self):
        text = self.text_box.get("1.0", "end").strip()
        if not text:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text file", "*.txt")],
            initialfile="ocr_result.txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self.status_label.configure(text="Saved ✓", text_color=SUCCESS)

    def _reset_btn(self):
        self.run_btn.configure(state="normal", text="  Run OCR ▶")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _sep(parent, row):
    ctk.CTkFrame(parent, fg_color=BORDER, height=1, corner_radius=0).grid(
        row=row, column=0, padx=20, pady=8, sticky="ew")

def _section_label(parent, text, row):
    ctk.CTkLabel(parent, text=text, font=("Helvetica", 10, "bold"),
                 text_color=TEXT_MUTED).grid(
        row=row, column=0, padx=24, pady=(12, 4), sticky="w")

def _mini_label(parent, text, row):
    ctk.CTkLabel(parent, text=text, font=("Helvetica", 11),
                 text_color=TEXT_MUTED).grid(
        row=row, column=0, pady=(4, 0), sticky="w")


if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
