import os
from flask import Flask, request, jsonify
import openai

# Load API Key from .env
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI API Key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize Flask app
app = Flask(__name__)

# Initialize conversation history for context
conversation_history = [{"role": "system", "content": "You are a negotiating chatbot."}]

# Define negotiation endpoint
@app.route('/negotiate', methods=['POST'])
def negotiate():
    user_offer = request.json.get('offer')
    if not user_offer:
        return jsonify({"error": "No offer provided"}), 400

    # Add user offer to conversation history
    user_message = f"The user offered ${user_offer}."
    conversation_history.append({"role": "user", "content": user_message})

    # Get chatbot response using GPT-4
    chatbot_response = get_chatbot_response(conversation_history)

    # Add chatbot's response to conversation history
    conversation_history.append({"role": "assistant", "content": chatbot_response})

    # Return response
    return jsonify({"response": chatbot_response})

def get_chatbot_response(conversation_history):
    # Let's set some pricing logic for the negotiation
    initial_price = 100  # Example starting price
    min_price = 70  # Minimum acceptable price
    
    # Extract the user offer from the history
    for message in conversation_history:
        if message['role'] == 'user':
            user_offer = extract_offer_from_message(message['content'])
    
    # Simple negotiation logic: chatbot responds with counteroffer
    if user_offer >= initial_price:
        response_text = f"The price of ${user_offer} is accepted."
    elif user_offer < min_price:
        response_text = f"The offer of ${user_offer} is too low. I can go no lower than ${min_price}."
    else:
        counteroffer = user_offer + (initial_price - user_offer) * 0.5  # 50% of the gap
        response_text = f"The offer of ${user_offer} is too low. How about ${counteroffer}?"

    return response_text

def extract_offer_from_message(message):
    # Simple helper function to extract numerical value from message
    return float(message.split('$')[1])


if __name__ == '__main__':
    app.run(debug=True)
