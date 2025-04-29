import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from parser import parse_graph_from_file, is_bipartite_graph
from hungarian import maximum_weight_matching_bipartite
from visualizer import draw_graph_with_matching

def load_and_process():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return

    try:
        G = parse_graph_from_file(file_path)

        if not is_bipartite_graph(G):
            raise ValueError("Graph is not bipartite or has inconsistent edges/weights.")

        matching, total_weight = maximum_weight_matching_bipartite(G)

        info_label.config(
            text=f"Maximum weight matching: {int(total_weight) if total_weight.is_integer() else total_weight}"
        )
        draw_graph_with_matching(G, matching, graph_frame)

    except ValueError as e:
        messagebox.showerror("Error", f"{str(e)}")
    except Exception as e:
        messagebox.showerror("Unexpected Error", "An unexpected error occurred. Please check your file format.\n\n" + str(e))
    finally:
        instruction_label.pack_forget()

root = tk.Tk()
root.title("Bipartite Graph Maximum Weight Matching")
root.geometry("1000x700")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x")

load_button = ttk.Button(button_frame, text="Load File", command=load_and_process)
load_button.pack()

instruction_label = tk.Label(
    main_frame,
    text="Text format:\nvertex : (neighbor, weight)\nExample:\na : (b, 5), (c, 3)\nb : (a, 5)\nc : (a, 3)",
    font=("Arial", 12),
    justify="left",
    fg="gray"
)
instruction_label.pack(pady=20)

info_label = tk.Label(main_frame, text="", font=("Arial", 14), fg="blue")
info_label.pack(pady=10)

graph_frame = ttk.Frame(main_frame)
graph_frame.pack(fill="both", expand=True)

root.mainloop()
