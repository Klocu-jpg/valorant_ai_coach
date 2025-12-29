import tkinter as tk

def show_summary(summary_text: str):
    root = tk.Tk()
    root.title("Valorant AI Coach - Post-Match Summary")
    root.geometry("500x400")

    text_widget = tk.Text(root, wrap="word", height=20, width=60)
    text_widget.insert(tk.END, summary_text)
    text_widget.config(state="disabled")  # make it read-only
    text_widget.pack(padx=10, pady=10, fill="both", expand=True)

    # Optional: close button
    tk.Button(root, text="Close", command=root.destroy).pack(pady=10)

    root.mainloop()