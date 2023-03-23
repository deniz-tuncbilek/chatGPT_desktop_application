import os
import openai
import customtkinter as ctk

openai.api_key = os.getenv("OPENAI_API_KEY")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class Bubble(ctk.CTkTextbox):
    def __init__(self, master, text, color):
        super().__init__(master)
        self.textbox = ctk.CTkTextbox(master=self, width=500, height=20,
                                      corner_radius=20,
                                      wrap='word', font=("Helvetica", 18),
                                      bg_color='transparent',
                                      fg_color=color
                                      )
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert('0.0', text)


class ScrollableBubbleFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.textbox_list = []
        self.grid_columnconfigure(3)

    def add_bubble(self, text, user):
        column = 0
        color = 'green'
        if user:
            column = 1
            color = 'blue'

        bubble = Bubble(master=self, text=text, color=color)
        bubble.grid(row=len(self.textbox_list), column=column, columnspan=2, pady=(0, 10))
        self.textbox_list.append(bubble)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.MESSAGES = [
            {"role": "system", "content": "You are a helpful assistant."}]

        self.title("OpenAI SimpleBot")
        self.resizable(False, False)
        self.grid_rowconfigure(2)
        self.grid_columnconfigure(3)

        self.my_frame = ScrollableBubbleFrame(master=self, width=1000,
                                              height=600, fg_color='transparent')
        self.my_frame.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        self.add_bubble('Welcome! Enter a prompt to continue...', user=False)

        self.entry = ctk.CTkEntry(self, height=40,
                                  font=("Helvetica", 18),
                                  placeholder_text="Enter your prompt...")
        self.entry.grid(row=1, column=0, columnspan=2, padx=(20, 10), pady=(0, 10), sticky="nsew")
        self.bind('<Return>', self.handle_generate)

        self.button = ctk.CTkButton(self, text="Generate",
                                    font=("Helvetica", 14), width=50)
        self.button.bind('<Button-1>', self.handle_generate)
        self.button.grid(row=1, column=2, padx=(0, 20), sticky="e")

    def add_bubble(self, text, user):
        self.my_frame.add_bubble(text, user)

    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=1000,
            messages=self.MESSAGES
        )
        return response.choices[0].message.content.strip()

    def handle_generate(self, event):
        user_input = self.entry.get().strip()
        if user_input:
            self.MESSAGES.append({"role": "user", "content": user_input})
            chatbot_response = self.generate_response(user_input)
            self.MESSAGES.append(
                {"role": "assistant", "content": chatbot_response})
            self.entry.delete(0, ctk.END)
            self.add_bubble(user_input, user=True)
            self.add_bubble(chatbot_response, user=False)


app = App()
app.mainloop()
