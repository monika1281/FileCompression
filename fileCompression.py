import tkinter as tk
from tkinter import filedialog
import heapq
import os

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(char=c, freq=f) for c, f in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, code="", mapping=None):
    if mapping is None:
        mapping = {}
    if node is not None:
        if node.char is not None:
            mapping[node.char] = code
        build_huffman_codes(node.left, code + "0", mapping)
        build_huffman_codes(node.right, code + "1", mapping)
    return mapping


def import_file(file_path, content_text):
    frequencies = {}
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()
        content_text.insert(tk.END, f"\n\n\n\n\n\nFile Read:\n\n{content}")

        for char in content:
            ascii_value = ord(char)
            print(f"Character: {char}, ASCII: {ascii_value}")
            
            frequencies[char] = frequencies.get(char, 0) + 1

    return frequencies


def encode(file_path, output_path, huffman_codes):
    with open(file_path, 'r') as input_file, open(output_path, 'wb') as output_file:
        encoded_data = ""
        for char in input_file.read():
            encoded_data += huffman_codes[char]
        padding = 8 - (len(encoded_data) % 8)
        encoded_data += "0" * padding
        for i in range(0, len(encoded_data), 8):
            byte = int(encoded_data[i:i + 8], 2)
            output_file.write(bytes([byte]))

def custom_message_box(message, title, background_color, text_color, width=500, height=720, x_offset=700, y_offset=40):
    custom_message_window = tk.Toplevel(root)
    custom_message_window.title(title)

    custom_message_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    label = tk.Label(custom_message_window, text=message, background=background_color, foreground=text_color, font=('Times 12'))
    label.pack(padx=10, pady=5)

    ok_button = tk.Button(custom_message_window, text="OK", command=custom_message_window.destroy, bg='#055636', fg='white')
    ok_button.pack(pady=5)


def compress_file(content_text):
    # Select file
    file_path = filedialog.askopenfilename(title="Select file to compress", filetypes=[("Text files", "*.txt")])
    if file_path:
        frequencies = import_file(file_path, content_text)
        huffman_tree = build_huffman_tree(frequencies)
        huffman_codes = build_huffman_codes(huffman_tree)

        # Create a frequency table string
        frequency_table = "Frequency Table:\n"
        for char, freq in frequencies.items():
            frequency_table += f"{char}: {freq}\n"

        output_path = file_path + ".huffman"
        encode(file_path, output_path, huffman_codes)

        original_size = os.path.getsize(file_path)
        compressed_size = os.path.getsize(output_path)

        compression_ratio = ((original_size - compressed_size) / original_size) * 100

        custom_message_box(
            f"File Read:\n{file_path}\n\n"
            f"Original Size: {original_size} bytes\n"
            f"Compressed Size: {compressed_size} bytes\n"
            f"Compression Ratio: {compression_ratio:.2f}%\n"
            f"{frequency_table}\n"
            f"Output saved to {output_path}",
            "Compression Complete",
            'purple',
            'white'
        )


# GUI
root = tk.Tk()

root.title("Huffman Compression")

root.configure(bg='#699986')

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

content_text = tk.Text(frame, height=18, width=60)
content_text.pack()
title_label = tk.Label(frame, text="   Select a file to compress  ",  bg='deep pink', fg="white", font=('Times 15'), pady=7)
title_label.place(x=25, y=35)
label = tk.Label(frame, text="File Read:",  bg='purple', fg="white", font=('Times 15'), pady=7)

compress_button = tk.Button(frame, text="Compress File", bg='#055636', fg="white", font=('Times 15'), command=lambda: compress_file(content_text))
compress_button.place(x=50, y=250)

root.mainloop()
