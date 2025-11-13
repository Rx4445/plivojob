from flask import Flask, Response, request, url_for, redirect, render_template_string
from plivo import plivoxml
import plivo


AUTH_ID = "MANZJJOGRLNZK0ZMZIMM"
AUTH_TOKEN = "ODU2MzY0MzkzZDFjN2U0ZjU5Y2U4NGViY2IwMWFh"
CALLER_ID = "+91 80 3127 4121" 
FORWARD_NUMBER = "918217044923" 
AUDIO_FILE_URL = "https://s3.amazonaws.com/plivocloud/Trumpet.mp3"

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plivo IVR Trigger</title>
    <style>
        body { font-family: sans-serif; display: grid; place-items: center; min-height: 90vh; background-color: #f4f4f9; }
        form { background: #fff; border: 1px solid #ccc; border-radius: 8px; padding: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
        h2 { margin-top: 0; text-align: center; }
        div { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"] { width: 300px; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        button { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <form action="/make-call" method="POST">
        <h2>InspireWorks IVR Demo</h2>
        <div>
            <label for="phone">Phone Number to Call:</label>
            <input type="text" id="phone" name="phone_number" placeholder="+15551234567">
        </div>
        <button type="submit">Start Call</button>
    </form>
</body>
</html>
"""

app = Flask(__name__)
client = plivo.RestClient(auth_id=AUTH_ID, auth_token=AUTH_TOKEN)


@app.route("/")
def homepage():
    """Serves the simple HTML form."""
    return render_template_string(HTML_FORM)


@app.route("/make-call", methods=["POST"])
def make_call():
    """Handles the form submission and redirects to the trigger route."""
    phone_to_call = request.form.get("phone_number")
    if not phone_to_call:
        return "Please go back and enter a phone number.", 400
    
    
    return redirect(url_for("trigger_call", phone_number=phone_to_call))



@app.route("/trigger-call/<phone_number>")
def trigger_call(phone_number):
    """Triggers the outbound call."""
    try:
       
        callback_url = request.url_root + 'welcome'
        
        print(f"Calling {phone_number}, using callback: {callback_url}")

        resp = client.calls.create(
            from_=CALLER_ID,
            to_=phone_number,
            answer_url=callback_url,
            answer_method="GET"
        )
        return f"Call triggered. Plivo request UUID: {resp['request_uuid']}"
    except Exception as e:
        return f"Error creating call: {e}", 500


@app.route("/welcome", methods=["GET", "POST"])
def welcome_menu():
    """Level 1: Language Selection"""
    r = plivoxml.ResponseElement()
    
    lang_menu = plivoxml.GetDigitsElement(
        action=request.url_root + 'handle-language', 
        method="GET",
        timeout=7,
        num_digits=1,
        retries=1
    )
    lang_menu.add(
        plivoxml.SpeakElement("For English, press 1. Para Español, presione 2.")
    )
    
    r.add(lang_menu)
   
    r.add(plivoxml.SpeakElement("No input detected. Goodbye."))
    return Response(r.to_string(), mimetype="text/xml")


@app.route("/handle-language", methods=["GET", "POST"])
def handle_language_choice():
    user_input = request.values.get("Digits")
    r = plivoxml.ResponseElement()

    if user_input not in ("1", "2"):
       
        r.add(plivoxml.SpeakElement("Invalid input."))
        r.add(plivoxml.RedirectElement(request.url_root + 'welcome'))
        return Response(r.to_string(), mimetype="text/xml")


    language_code = "en" if user_input == "1" else "es"

    
    action_menu = plivoxml.GetDigitsElement(
       
        action=request.url_root + f'handle-action?lang={language_code}', 
        method="GET",
        timeout=7,
        num_digits=1,
        retries=1
    )

    if language_code == "en":
        menu_text = "Press 1 to play a short audio message. Press 2 to connect to a live associate."
    else:
        menu_text = "Presione 1 para reproducir un breve mensaje de audio. Presione 2 para conectarse con un asociado."

    action_menu.add(plivoxml.SpeakElement(menu_text))
    r.add(action_menu)
    r.add(plivoxml.SpeakElement("No input detected. Goodbye."))
    return Response(r.to_string(), mimetype="text/xml")


@app.route("/handle-action", methods=["GET", "POST"])
def handle_action_choice():
    user_input = request.values.get("Digits")
    language_code = request.args.get("lang", "en") 
    r = plivoxml.ResponseElement()

    if user_input == "1":
     
        if language_code == "en":
            r.add(plivoxml.SpeakElement("Playing audio. Goodbye."))
        else:
            r.add(plivoxml.SpeakElement("Reproduciendo audio. Adiós."))
        r.add(plivoxml.PlayElement(AUDIO_FILE_URL))
     
        
    elif user_input == "2":
      
        dial_element = plivoxml.DialElement()
        dial_element.add(plivoxml.NumberElement(FORWARD_NUMBER))
        if language_code == "en":
            r.add(plivoxml.SpeakElement("Connecting you now."))
        else:
            r.add(plivoxml.SpeakElement("Conectando ahora."))
        r.add(dial_element)
      

    else:
       
        r.add(plivoxml.SpeakElement("Invalid choice."))
        r.add(plivoxml.RedirectElement(request.url_root + f'handle-language?lang={language_code}'))

    return Response(r.to_string(), mimetype="text/xml")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)