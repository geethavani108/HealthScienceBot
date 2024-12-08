import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize OpenAI API
openai.api_key = 'sample_open_ai_key'

# Example data storage for appointments and user data
appointments = []
user_data = {}

# Frequently Asked Questions (FAQs)
faqs = {
    "what are your business hours": "Our business hours are 9 AM to 6 PM, Monday to Saturday.",
    "where are you located": "We are located at 1234 Health Lane, MedCity.",
    "how can I contact support": "You can contact our support team at support@healthcompany.com or call us at +1234567890.",
    "what services do you offer": "We offer a range of health science services including consultations, diagnostics, and treatment plans."
}

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
def generate_response(intent, user_input, user_name=None):
    if intent == "appointment":
        return f"Sure, {user_name if user_name else 'I'} can help you with an appointment. Please provide your preferred date and time."
    elif intent == "support":
        if user_input.lower() in faqs:
            return faqs[user_input.lower()]
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
        return faqs["what are your business hours"]
    elif intent == "location":
        return faqs["where are you located"]
    else:
        if user_input.lower() in faqs:
            return faqs[user_input.lower()]
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

# Function to check if appointment time is available
def is_time_available(time):
    for appointment in appointments:
        if appointment['time'] == time:
            return False
    return True

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_id = request.json.get('user_id')
    intent = classify_intent(user_input)

    # Retrieve or initialize user data
    user = user_data.get(user_id, {})
    user_name = user.get('name')

    if intent == "appointment" and "name" in request.json and "time" in request.json:
        name = request.json.get('name')
        time = request.json.get('time')
        if is_time_available(time):
            appointments.append({"name": name, "time": time})
            response = f"Appointment booked for {name} at {time}."
        else:
            response = f"Sorry, the time {time} is already booked. Please choose a different time."
    else:
        response = generate_response(intent, user_input, user_name)
    
    # Save user name if provided
    if "name" in request.json:
        user_data[user_id] = user_data.get(user_id, {})
        user_data[user_id]['name'] = request.json['name']

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
