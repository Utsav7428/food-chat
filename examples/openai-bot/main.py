from textbase import bot, Message
import openai



# Set your OpenAI API key
openai.api_key = "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"

# Create a bot using the @bot() decorator
@bot()
def on_message(message_history, state=None):
    # Extract the latest user message
    user_message = message_history[-1].content if message_history else ""

    # Check if the user message contains a food preference
    if "preference:" in user_message.lower():
        # Extract the user's food preference
        user_preference = user_message.split("preference:", 1)[1].strip()

        # Generate a food recommendation using the OpenAI API
        recommended_food = recommend_food(user_preference)

        # Create the bot response
        bot_response = f"I recommend trying {recommended_food} based on your preference for {user_preference} food."
    else:
        bot_response = "Please specify your food preference by typing 'Preference: [Your preference].'"

    # Create the response JSON structure
    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": [
            {
                "message": ""
            }
        ]
    }

    return {
        "status_code": 200,
        "response": response
    }

def recommend_food(user_preference):
    # Define a system prompt for OpenAI
    system_prompt = f"You are a food recommendation bot. The user prefers {user_preference} food. Suggest a food item."

    # Generate a food recommendation using the OpenAI GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=system_prompt,
        max_tokens=50,  # Adjust as needed for the desired response length
        n=1  # Generate a single response
    )

    # Extract the recommended food item from the response
    recommended_food = response.choices[0].text.strip()

    return recommended_food

# Run the chatbot
if __name__ == "__main__":
    import uvicorn

    # Start the bot server using uvicorn
    uvicorn.run("your_script_name:app", host="0.0.0.0", port=8000)
