import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Deine Keywords (ohne "orchestra")
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

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def check():
    found = []
    for url in URLS:
        try:
            r = requests.get(url, timeout=15)
            text = r.text.lower()
            for word in KEYWORDS:
                if word in text:
                    found.append(f"{word} gefunden auf {url}")
        except:
            pass
    return list(set(found))

if __name__ == "__main__":
    results = check()
    if results:
        message = "🎮 Neue Game Concert Treffer:\n\n" + "\n".join(results)
        send_telegram(message)
