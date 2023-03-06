import openai
import os
import customtkinter as ctk

openai.api_key = os.getenv("OPENAI_API_KEY")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ChatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.MESSAGES = [{"role": "system", "content": "You are a helpful assistant."}]

        self.title("OpenAI SimpleBot")
        self.resizable(False, False)

        self.chat_box = ctk.CTkTextbox(self, width=600, height=600, font=("Helvetica",18))
        self.chat_box.grid(row=0, column=0, columnspan=2)

        self.entry = ctk.CTkEntry(self, width=510, font=("Helvetica",18))
        self.entry.grid(row=1, column=0)
        self.bind('<Return>', self.handle_generate)

        self.button = ctk.CTkButton(self, text="Generate", width=50)
        self.button.bind('<Button-1>', self.handle_generate)
        self.button.grid(row=1, column=1)


    def generate_response(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=1000,
            messages=self.MESSAGES
        )
        return response.choices[0].message.content.strip()


    def handle_generate(self, event1):
        user_input = self.entry.get().strip()
        if user_input:
            self.MESSAGES.append({"role": "user", "content": user_input})
            chatbot_response = self.generate_response(user_input)
            self.MESSAGES.append({"role": "assistant", "content": chatbot_response})
            self.entry.delete(0, ctk.END)
            self.chat_box.insert(ctk.END, "You:\r\n\t" + user_input + "\r\n")
            self.chat_box.insert(ctk.END, "ChatGPT:\r\n\t" + chatbot_response + "\r\n")



if __name__ == "__main__":
    chat = ChatGUI()
    chat.mainloop()

