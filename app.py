import chainlit as cl
import pandas as pd
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Dictionary to store DataFrames by username
user_dataframes = {}

@cl.on_chat_start
async def start_chat():
    await cl.Message(content="Hello! I am your chat code interpreter. Say Hi! to get started.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    username = message.id  # Get the username

    files = None

    # Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a csv file to begin!", 
            accept=["text/csv"],
            max_size_mb = 100,
        ).send()

    file = files[0]

    # Check if the message contains a file
    if file:
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file.path)

            # Store the DataFrame in the global dictionary using username as the key
            user_dataframes[username] = df

            # Send a confirmation message
            await cl.Message(content="CSV file uploaded successfully. Now, please enter the Python code to run on the CSV data.").send()
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            await cl.Message(content=f"An error occurred while reading the CSV file: {str(e)}").send()
    else:
        # Check if the user has already uploaded a CSV file
        if username not in user_dataframes:
            await cl.Message(content="No CSV file uploaded. Please upload a CSV file first.").send()
            return

    # Retrieve the DataFrame from the global dictionary
    df = user_dataframes[username]

    # Get the user-provided code
    code = message.content

    # Prepare the prompt for OpenAI
    prompt = f"Given the following DataFrame `df`:\n\n{df.head()}\n\nExecute the following Python code and return the output:\n\n{code}"

    try:
        # Call OpenAI API to execute the code
        response = openai.completions.create(
                model="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.5
            )

        # Extract the response text
        output = response.choices[0].text.strip()

        # Send the output back to the user
        await cl.Message(content=f"Output:\n{output}").send()
    except Exception as e:
        print(f"Error executing code: {e}")
        await cl.Message(content=f"An error occurred while executing the code: {str(e)}").send()

if __name__ == '__main__':
    cl.run()