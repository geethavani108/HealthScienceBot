

#pip install openai==0.28
#pip install requests


# health_science_chatbot.py
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = 'sample_open_ai_key'


# Example data storage for appointments
appointments = []

# Function to classify intent
def classify_intent(user_input):
    user_input = user_input.lower()
    if "appointment" in user_input or "book" in user_input:
        return "appointment"
    elif "support" in user_input or "help" in user_input:
        return "support"
    elif "hours" in user_input or "time" in user_input:
        return "hours"
    elif "location" in user_input or "where" in user_input:
        return "location"
    else:
        return "general"

# Function to generate a response using GPT-3
def generate_response(intent, user_input):
    if intent == "appointment":
        return "Sure, I can help you with an appointment. Please provide your name and preferred date and time."
    elif intent == "support":
        prompt = f"Customer support for health science company:\nCustomer: {user_input}\nSupport:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    elif intent == "hours":
        return "Our business hours are 9 AM to 6 PM, Monday to Saturday."
    elif intent == "location":
        return "We are located at 1234 Health Lane, MedCity."
    else:
        prompt = f"Customer support for health science company:\nCustomer: {user_input}\nSupport:"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    intent = classify_intent(user_input)

    if intent == "appointment" and "name" in request.json and "time" in request.json:
        name = request.json.get('name')
        time = request.json.get('time')
        appointments.append({"name": name, "time": time})
        response = f"Appointment booked for {name} at {time}."
    else:
        response = generate_response(intent, user_input)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

