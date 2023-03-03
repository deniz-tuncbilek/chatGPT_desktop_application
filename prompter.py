import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

while True:
    user_input = input("Enter a command or press q to quit:\n")
    if user_input.lower() == 'q':
        break

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=1500,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    print(response.choices[0].message.content.strip())
