InspireWorks Plivo IVR Demo

This is a simple web application built with Python and Flask to demonstrate a multi-level IVR system using Plivo's Voice APIs and XML.

The application provides a simple web form to trigger an outbound call. When the call is answered, the user is guided through a multi-level IVR menu to select a language and then choose an action (either play audio or connect to an associate).

Features

Web-based Trigger: A simple HTML form to initiate the outbound call.

Level 1 IVR: Language selection (English/Spanish).

Level 2 IVR: Action selection (Play Audio / Forward Call).

XML Generation: All call flow logic is handled by generating Plivo XML (PHLOXML) on the fly.

Invalid Input Handling: The menus will gracefully handle invalid key presses.

Setup Instructions

Clone or Download:
Download the app.py file from this repository.

Install Dependencies:
This project requires Python 3, plivo, and flask.

pip install plivo
pip install flask


Install Ngrok:
Download ngrok from ngrok.com to create a public URL for your local server.

Enter Credentials:
Open the app.py file and fill in your Plivo credentials in the configuration section at the top:

AUTH_ID: Your Plivo Auth ID.

AUTH_TOKEN: Your Plivo Auth Token.

CALLER_ID: A Plivo voice-enabled phone number (e.g., +15551234567).

FORWARD_NUMBER: A real phone number to test the call forwarding (e.g., your cell phone, +15551234567).

Note: Do not commit your secret AUTH_TOKEN to a public GitHub repository.

Steps to Run and Test

You will need two terminals (command prompts) running at the same time.

Terminal 1: Run the Flask Server

Navigate to the project folder.

Run the application:

python app.py


The server will start on http://localhost:5000. Leave this terminal running.

Terminal 2: Run Ngrok

Open a new terminal.

Start ngrok to create a public tunnel to your server:

ngrok http 5000


ngrok will give you a public "Forwarding" URL. Copy the https://... URL.
(e.g., https://random-name.ngrok-free.app)

Step 3: Test the Application

Open your web browser.

Paste your ngrok URL into the address bar and press Enter.

You will see the "InspireWorks IVR Demo" web form.

In the "Phone Number to Call" box, type in your cell phone number (e.g., +15551234567).

Click the "Start Call" button.

Your cell phone will ring. Answer it (on speaker) and follow the IVR prompts to test all the paths.