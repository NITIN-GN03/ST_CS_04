import tkinter as tk
from tkinter import messagebox, filedialog
import datetime
import os

LOGFILE = "key_log.txt"

class KeyLoggerApp:
    def __init__(self, root):
        self.root = root
        root.title("Safe Key Logger Demo - In-App Only")
        root.geometry("700x450")

        # Top frame with buttons
        top = tk.Frame(root)
        top.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        self.start_btn = tk.Button(top, text="Start Logging", command=self.start_logging)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = tk.Button(top, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Save Log As...", command=self.save_log_as).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Open Log File", command=self.open_log_file).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="Clear Log File", command=self.clear_log_file).pack(side=tk.LEFT, padx=4)
        tk.Button(top, text="About / Safety", command=self.show_about).pack(side=tk.RIGHT, padx=4)

        # Text area
        self.text = tk.Text(root, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
        self.text.insert("1.0", "Type here. Only keys typed inside this box are recorded to the log file.\n\n")

        # Status bar
        self.status = tk.Label(root, text="Stopped", anchor="w")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Logging state
        self.logging = False
        # Bind key event to text widget only (so we don't capture global keystrokes).
        self.text.bind("<Key>", self.on_key)

    def start_logging(self):
        self.logging = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text="Logging: started")
        # Add a header to the log file
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write("\n=== Logging started at {} ===\n".format(datetime.datetime.now()))

    def stop_logging(self):
        self.logging = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="Stopped")
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write("=== Logging stopped at {} ===\n".format(datetime.datetime.now()))

    def on_key(self, event):
        # Only record when logging is active. event.char is the character (empty for special keys)
        if not self.logging:
            return
        key = event.keysym  # e.g., 'a', 'Return', 'BackSpace'
        char = event.char
        timestamp = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
        # Create a friendly representation
        if char and char.isprintable():
            entry = f"{timestamp}\tCHAR\t{char}\n"
        else:
            entry = f"{timestamp}\tKEY\t<{key}>\n"
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(entry)

    def save_log_as(self):
        if not os.path.exists(LOGFILE):
            messagebox.showinfo("No log", "No log file found yet. Start logging to create a log.")
            return
        dst = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files","*.txt"),("All files","*.*")])
        if dst:
            try:
                with open(LOGFILE, "r", encoding="utf-8") as srcf, open(dst, "w", encoding="utf-8") as dstf:
                    dstf.write(srcf.read())
                messagebox.showinfo("Saved", f"Log saved to {dst}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def open_log_file(self):
        if not os.path.exists(LOGFILE):
            messagebox.showinfo("No log", "No log file found yet.")
            return
        try:
            os.startfile(LOGFILE)  # Works on Windows
        except Exception:
            # Fallback: show contents in a simple dialog
            with open(LOGFILE, "r", encoding="utf-8") as f:
                content = f.read()
            show = tk.Toplevel(self.root)
            show.title("Log File Contents")
            txt = tk.Text(show, wrap=tk.WORD)
            txt.pack(fill=tk.BOTH, expand=True)
            txt.insert("1.0", content)

    def clear_log_file(self):
        if messagebox.askyesno("Clear log", "Are you sure you want to clear the log file?"):
            open(LOGFILE, "w", encoding="utf-8").close()
            messagebox.showinfo("Cleared", "Log file cleared.")

    def show_about(self):
        messagebox.showinfo("About / Safety",
                            ("This is a SAFE demo that records ONLY keys typed inside this application's text box.\n\n"
                             "It does NOT capture global/system keystrokes. Use ethically and only on your own machine."))

if __name__ == '__main__':
    root = tk.Tk()
    app = KeyLoggerApp(root)
    root.mainloop()
