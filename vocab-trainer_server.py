from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from os import environ
from markupsafe import escape
import random

app = Flask(__name__)

app.secret_key = environ.get("SECRET_KEY", "fallback-key")
app.config["DEBUG"] = False
app.config["ENV"] = "production"

# Vocabulary dictionary with multiple translations
vocabulary = {
    "dojeżdżać do pracy": ["commute"],
    "mieć widok na": ["overlook"],
    "sąsiedztwo": ["neighbourhood"],
    "sąsiad": ["neighbour"],
    "dzielnica": ["district"],
    "na przedmieściach": ["in the suburbs"],
    "w centrum miasta": ["in the city centre"],
    "na skraju, na obrzeżach": ["on the edge"],
    "mieszkaniec": ["inhabitant"],
    "najemca, lokator": ["tenant"],
    "położony w": ["located in"],
    "agent nieruchomości": ["estate agent"],
    "hipoteka": ["mortgage"],
    "parapetówka": ["housewarming party"],
    "dzielić pokój z": ["share a room with"],
    "dzielić mieszkanie z": ["share a flat with"],
    "wprowadzić się": ["move in"],
    "wyprowadzić się": ["move out"],
    "współlokator mieszkaniowy": ["flatmate"],
    "współlokator 'pokojowy'": ["room-mate"],
    "zakwaterowanie": ["accommodation"],
    "wynająć / czynsz": ["rent"],
    "płacić czynsz": ["pay the rent"],
    "meblować": ["furnish"],
    "umeblowany": ["furnished"],
    "wyposażony": ["equipped"],
    "sprzęt (np., naczynia)": ["utensils"],
    "zmywarka": ["dishwasher"],
    "pralka": ["washing machine"],
    "szafa, garderoba": ["wardrobe"],
    "tapeta": ["wallpaper"],
    "kuchenka": ["cooker"],
    "lodówka": ["fridge"],
    "lustro": ["mirror"],
    "dywanik / chodniczek": ["rug"],
    "kaloryfer": ["radiator"],
    "poduszka": ["pillow"],
    "wyposażenie": ["equipment"],
    "odkurzacz": ["hoover", "vacuum cleaner"],
    "wygodny": ["comfortable"],
    "mały / drobniutki": ["tiny"],
    "przytulny": ["cosy", "homely"],
    "przestronny": ["spacious"],
    "nowoczesny": ["modern"],
    "drewniany": ["wooden"],
    "dobrze utrzymany": ["well-maintained"],
    "odnowiony, wykończony": ["decorated"],
    "osiedle mieszkaniowe": ["housing estate"],
    "rezydencja": ["mansion"],
    "domek jednorodzinny": ["detached house"],
    "domek na wsi": ["cottage"],
    "kawalerka": ["bedsit"],
    "łazienka": ["bathroom"],
    "gabinet (do pracy w domu)": ["study"],
    "meble": ["furniture"],
    "jasny": ["bright"],
    "zagracony": ["cluttered"],
    "przerobić, przekształcić": ["convert"],
    "płacić z góry/zaliczkę": ["pay in advance"],
    "mieszkać samemu (np., Mieszkam sam.)": ["live on one's own"],
    "ścielić łóżko":["make the bed"],
    "prasować ubrania":["iron the clothes"],
    "wykonywać prace w domu (np. zmywać)":["do the housework"],
    "kosić trawnik":["mow the lawn"],
    "uroki, udogodnienia":["amenities"],
    "urządzenia (elektryczne)":["appliances"],
    "sprzęt":["utensils"]
}

# Track user progress
progress = {word: 0 for word in vocabulary}

# Queue for repeating difficult words
queue = []

# Theme toggle route
#@app.route('/set_theme', methods=["POST"])
#def set_theme():
#    theme = request.json.get("theme", "light")  # Default to light
#    session["theme"] = theme  # Store in session
#    return jsonify({"message": "Theme updated!", "theme": theme}), 200

@app.route("/")
def home():
#    theme = session.get("theme", "auto")  # Default to auto-detection
    return render_template("index.html")

@app.after_request
def add_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'"
    return response

@app.errorhandler(404)
def not_found(error):
    return "Page not found.", 404

@app.errorhandler(500)
def server_error(error):
    return "Internal server error.", 500

@app.route('/flashcards', methods=["GET", "POST"])
def flashcards():
    global queue
    if not queue:
        queue = list(vocabulary.items())
        random.shuffle(queue)

    if request.method == "POST":
        if "show_answer" in request.form:
            polish = request.form["polish"]
            return render_template("flashcards.html", polish=polish, english=", ".join(vocabulary[polish]), show_answer=True)

        polish = request.form["polish"]
        known = request.form["known"]
        
        if known == "yes":
            progress[polish] += 1
        else:
            queue.append((polish, vocabulary[polish]))  # Re-add unknown words

        return redirect(url_for("flashcards"))

    if queue:
        polish, english_list = queue.pop(0)
        return render_template("flashcards.html", polish=polish, show_answer=False)

    return "Ukończyłeś wszystkie fiszki."


@app.route('/test', methods=["GET", "POST"])
def test():
    if request.method == "POST":
        polish = escape(request.form.get("polish", ""))
        answer = escape(request.form.get("answer", "")).lower().strip()

        if polish not in vocabulary:
            return "Błendeł (wina motocyklisty)."

        correct_answers = [e.lower() for e in vocabulary[polish]]

        if answer in correct_answers:
            progress[polish] += 1
            result = "Poprawnie!"
        else:
            result = f"Źle! Poprawna odpowiedź to: {', '.join(vocabulary[polish])}"

        return render_template("test.html", result=result)

    polish, correct = random.choice(list(vocabulary.items()))
    return render_template("test.html", polish=polish)

if __name__ == '__main__':
    app.run(debug=False)
