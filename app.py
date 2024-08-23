

from flask import Flask, render_template, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask(__name__)

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER") 
TWILIO_SMS_NUMBER = os.getenv("TWILIO_SMS_NUMBER")  # e.g., '+1234567890'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()

# Helper function to send WhatsApp message
def send_whatsapp_message(to_number, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        print(f"WhatsApp message sent to {to_number}")
    except Exception as e:
        print(f"Error sending WhatsApp message: {e}")

# Helper function to send SMS message
def send_sms_message(to_number, message):
    try:
        client.messages.create(
            body=message,
            from_=TWILIO_SMS_NUMBER,
            to=to_number
        )
        print(f"SMS sent to {to_number}")
    except Exception as e:
        print(f"Error sending SMS: {e}")
    
# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to schedule message
@app.route('/schedule_message', methods=['POST'])
def schedule_message():
    data = request.json
    recipient_number = data.get('recipientNumber')
    message = data.get('message')
    sender_name = data.get('senderName')
    recipient_name = data.get('recipientName')
    schedule_date = data.get('scheduleDate')
    schedule_time = data.get('scheduleTime')
    message_type = data.get('messageType')  # New field to choose between SMS or WhatsApp

    if not all([recipient_number, message, sender_name, recipient_name, schedule_date, schedule_time, message_type]):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    # Combine date and time into datetime object
    try:
        schedule_datetime = datetime.strptime(f"{schedule_date} {schedule_time}", "%Y-%m-%d %H:%M")
    except ValueError as e:
        print(f"Error parsing date/time: {e}")
        return jsonify({'status': 'error', 'message': 'Invalid date or time format'}), 400

    # Schedule the job based on message type
    if message_type == 'whatsapp':
        scheduler.add_job(func=send_whatsapp_message, args=[recipient_number, f"Hi {recipient_name}, {message} - From {sender_name}"], trigger='date', run_date=schedule_datetime)
    elif message_type == 'sms':
        scheduler.add_job(func=send_sms_message, args=[recipient_number, f"Hi {recipient_name}, {message} - From {sender_name}"], trigger='date', run_date=schedule_datetime)
    else:
        return jsonify({'status': 'error', 'message': 'Invalid message type'}), 400

    print(f"Scheduled {message_type} message for {recipient_name} at {schedule_datetime}")
    return jsonify({'status': 'success', 'message': f'{message_type.capitalize()} message scheduled successfully'})

if __name__ == '__main__':
    app.run(debug=True)
