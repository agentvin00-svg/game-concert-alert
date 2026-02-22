import requests
import os

# Telegram Daten aus GitHub Secrets
TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Keywords (ohne "orchestra")
KEYWORDS = [
    "metal gear solid",
    "kingdom come deliverance",
    "kcd2",
    "kingdom come deliverance 2",
    "battlefield",
    "video game concert",
    "game music",
    "gaming concert"
]

# Webseiten, die durchsucht werden
URLS = [
    "https://www.ticketmaster.de/search?q=game",
    "https://www.ticketmaster.co.uk/search?q=game",
    "https://www.eventim.de/de/search/?q=game",
]

# Funktion, um Telegram Nachricht zu senden
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data, timeout=10)
        print("DEBUG: Telegram Response Code =", r.status_code)
    except Exception as e:
        print("DEBUG: Fehler beim Senden der Nachricht:", e)

# Funktion, um Treffer zu suchen
def check():
    found = []
    for url in URLS:
        try:
            r = requests.get(url, timeout=15)
            text = r.text.lower()
            for word in KEYWORDS:
                if word in text:
                    found.append(f"{word} gefunden auf {url}")
        except Exception as e:
            print("DEBUG: Fehler beim Abrufen von", url, e)
    return list(set(found))

# Hauptprogramm
if __name__ == "__main__":
    results = check()
    
    # Debug-Ausgabe in GitHub Logs
    print("DEBUG: Ergebnisse =", results)
    
    if results:
        message = "🎮 Neue Game Concert Treffer:\n\n" + "\n".join(results)
        send_telegram(message)
    else:
        send_telegram("ℹ️ Heute leider nichts gefunden. Alles funktioniert aber korrekt ✅")
