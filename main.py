import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Menu
import requests
import threading
import re
import json
import pyperclip

class OllamaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ollama Chat")
        self.root.geometry("1000x800")

        self.chat_history = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, state='disabled',
            font=('Arial', 12), padx=10, pady=10
        )
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.configure_text_styles()

        input_frame = ttk.Frame(root)
        input_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Text(
            input_frame, wrap=tk.WORD, 
            height=4, font=('Arial', 12),
            padx=10, pady=10
        )
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.user_input.bind("<Shift-Return>", lambda e: self.user_input.insert(tk.INSERT, "\n"))
        self.user_input.bind("<Control-Return>", lambda e: self.send_message())

        button_frame = ttk.Frame(input_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.send_button = ttk.Button(
            button_frame, text="Send (Ctrl+Enter)", 
            command=self.send_message
        )
        self.send_button.pack(pady=5)
        
        clear_button = ttk.Button(
            button_frame, text="Clear Input", 
            command=self.clear_input
        )
        clear_button.pack(pady=5)

        self.model_var = tk.StringVar()
        self.model_dropdown = ttk.Combobox(root, textvariable=self.model_var, state='readonly')
        self.model_dropdown.pack(padx=10, pady=5, fill=tk.X)

        self.status_var = tk.StringVar()
        ttk.Label(root, textvariable=self.status_var, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
        self.create_context_menu()

        self.typing_dots = 0 
        self.messages = []
        self.typing_active = False
        self.current_response = []
        self.response_position = None
        self.load_models()

    def configure_text_styles(self):
        self.chat_history.tag_configure('code', 
            background='#f0f0f0', 
            font=('Consolas', 11),
            borderwidth=1,
            lmargin1=20,
            lmargin2=20,
            spacing3=5
        )
        self.chat_history.tag_configure('user', foreground='#2c3e50')
        self.chat_history.tag_configure('assistant', foreground='#2980b9')
        self.chat_history.tag_configure('typing', foreground='#7f8c8d')
        self.chat_history.tag_configure('think', 
            background='#fff3cd',
            relief='solid',
            borderwidth=1,
            lmargin1=10,
            lmargin2=10,
            spacing1=5,
            spacing3=5
        )

    def create_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.chat_history.bind("<Button-3>", self.show_context_menu)
        self.user_input.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def copy_text(self):
        widget = self.root.focus_get()
        if widget in [self.chat_history, self.user_input]:
            widget.event_generate("<<Copy>>")

    def load_models(self):
        def fetch_models():
            try:
                response = requests.get("http://localhost:11434/api/tags")
                models = [model["name"] for model in response.json()["models"]]
                self.root.after(0, lambda: self.update_models(models))
                self.status_var.set("Ready")
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load models: {e}"))
        
        self.status_var.set("Loading models...")
        threading.Thread(target=fetch_models, daemon=True).start()

    def update_models(self, models):
        self.model_dropdown['values'] = models
        if models:
            self.model_var.set(models[0])
        else:
            messagebox.showwarning("No Models", "No Ollama models found")

    def start_typing_animation(self):
        self.typing_active = True
        self.update_typing_indicator()

    def update_typing_indicator(self):
        if self.typing_active:
            dots = (self.typing_dots % 3) + 1
            self.status_var.set(f"Assistant is typing{'.' * dots}")
            self.typing_dots += 1
            self.root.after(500, self.update_typing_indicator)

    def stop_typing_indicator(self):
        self.typing_active = False
        self.status_var.set("Ready")


    def format_response(self, text):
        start = self.chat_history.index("insert linestart")
        end = self.chat_history.index("end")
        self.chat_history.delete(start, end)

        parts = re.split(r'(<think>[\s\S]*?</think>|```[\s\S]*?```)', text)
        for part in parts:
            if not part:
                continue
            if part.startswith('<think>'):
                content = re.sub(r'<think>|</think>', '', part).strip()
                self.insert_think_block(content)
            elif part.startswith('```'):
                language = part.split('\n')[0][3:] or ''
                code = '\n'.join(part.split('\n')[1:-1]).strip()
                self.insert_code_block(code, language)
            else:
                self.chat_history.insert(tk.END, part.strip() + '\n', 'assistant')

    def insert_think_block(self, content):
        current_pos = self.chat_history.index(tk.INSERT)
        line_start = self.chat_history.index(f"{current_pos} linestart")
        
        if current_pos != line_start:
            self.chat_history.insert(tk.END, "\n")

        self.chat_history.insert(tk.END, "🤔 Thinking:\n", 'think')
        self.chat_history.insert(tk.END, f"{content}\n", 'think')
        self.chat_history.insert(tk.END, "\n")  

    def insert_code_block(self, code):
        self.chat_history.insert(tk.END, f"\n{code}\n", 'code')
        btn = ttk.Button(self.chat_history, text="📋 Copy", 
                       command=lambda c=code: self.copy_code(c),
                       style='Copy.TButton')
        self.chat_history.window_create(tk.END, window=btn)
        self.chat_history.insert(tk.END, "\n")

    def copy_code(self, code):
        pyperclip.copy(code)
        self.status_var.set("Code copied to clipboard!")
        self.root.after(2000, lambda: self.status_var.set("Ready"))

    def clear_input(self):
        self.user_input.delete('1.0', tk.END)

    def send_message(self):
        user_text = self.user_input.get('1.0', tk.END).strip()
        model = self.model_var.get()
        
        if not user_text:
            return
        if not model:
            messagebox.showwarning("No Model", "Please select a model first")
            return
        
        self.clear_input()
        self.messages.append({"role": "user", "content": user_text})
        self.update_chat_display("user", user_text)
        
        self.user_input.config(state='disabled')
        self.send_button.config(state='disabled')
        self.start_typing_animation()
        self.current_response = []
        self.response_position = None
        
        threading.Thread(target=self.stream_ollama_response, args=(model,), daemon=True).start()

    def stream_ollama_response(self, model):
        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": self.messages,
                    "stream": True
                },
                stream=True
            )
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8'))
                    content = chunk.get("message", {}).get("content", "")
                    full_response += content
                    self.current_response.append(content)
                    self.root.after(0, lambda c=content: self.stream_response(c))
                    
                    if chunk.get("done", False):
                        break

            self.root.after(0, self.finalize_response, full_response)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"API Error: {e}"))
            self.root.after(0, self.cancel_response)
        finally:
            self.root.after(0, self.stop_typing_indicator)
            self.root.after(0, self.enable_input)

    def stream_response(self, content):
        self.chat_history.configure(state='normal')
        
        if not self.response_position:
            self.chat_history.mark_set('assistant_start', tk.END)
            self.chat_history.insert(tk.END, "Assistant:\n", 'assistant')
            self.response_position = self.chat_history.index(tk.END)
        
        pos = self.chat_history.index(tk.END)
        self.chat_history.insert(self.response_position, content, 'typing')
        self.chat_history.delete(pos, tk.END) 
        
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def finalize_response(self, full_response):
        self.messages.append({"role": "assistant", "content": full_response})

        self.chat_history.configure(state='normal')
        self.chat_history.delete(1.0, tk.END)
        
        for msg in self.messages:
            if msg["role"] == "user":
                self.chat_history.insert(tk.END, f"You:\n{msg['content']}\n\n", 'user')
            elif msg["role"] == "assistant":
                self.chat_history.insert(tk.END, "Assistant:\n", 'assistant')
                self.format_response(msg['content'])
                self.chat_history.insert(tk.END, "\n\n")  
        
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

    def cancel_response(self):
        self.chat_history.configure(state='normal')
        if self.response_position:
            self.chat_history.delete('assistant_start', 'end')
        self.chat_history.configure(state='disabled')
        self.current_response = []
        self.response_position = None

    def enable_input(self):
        self.user_input.config(state='normal')
        self.send_button.config(state='normal')
        self.user_input.focus()

    def update_chat_display(self, role, content):
        self.chat_history.configure(state='normal')
        if role == "user":
            self.chat_history.insert(tk.END, f"You:\n{content}\n\n", 'user')
        else:
            self.chat_history.insert(tk.END, "Assistant:\n", 'assistant')
            self.chat_history.insert(tk.END, "Typing...\n\n", 'typing')
        self.chat_history.configure(state='disabled')
        self.chat_history.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.configure('Copy.TButton', 
                   font=('Arial', 8),
                   padding=2,
                   relief='flat',
                   background='#e1e1e1')
    app = OllamaGUI(root)
    root.mainloop()