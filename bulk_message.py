import pandas as pd
import requests, time, re
from bs4 import BeautifulSoup
import pywhatkit
import pyautogui  


CSV_PATH        = "contacts.xlsx"
OLLAMA_MODEL    = "mistral"     # change to "llama3" or any local model you prefer
OLLAMA_URL      = "http://localhost:11434/api/generate"
MAX_PARAS       = 3             # paragraphs to include from site
WAIT_BETWEEN    = 10         # seconds between WhatsApp sends


def sanitize_url(url: str) -> str:
    if not re.match(r"^https?://", url, re.I):
        url = "http://" + url
    return url

def scrape_website(url: str) -> str:
    """Return 'Title: ...\\nContent: ...' or fallback message."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title   = (soup.title.string or "").strip() if soup.title else ""
        paras   = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
        content = " ".join(paras[:MAX_PARAS])

        summary = f"Title: {title}\nContent: {content[:600]}"
        return summary if title or content else "No significant content found."
    except Exception as e:
        print(f"[!] Could not scrape {url}: {e}")
        return "Could not fetch website content."

def query_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    """Call local Ollama model and return generated text."""
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=120)
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception as e:
        print(f"[!] Ollama error: {e}")
        return ""

def build_prompt(name: str, site_snapshot: str) -> str:
    return f"""
You are a friendly digital‑marketing consultant.

Create a concise (≈60‑100 words) WhatsApp message for {name}, the owner of the business described below. 
• Mention one specific positive observation from the website snapshot. 
• Offer a clear benefit (e.g., increasing leads, improving SEO, running paid ads). 
• End with an invitation to chat on WhatsApp.

Website snapshot:
{site_snapshot}
"""

def send_whatsapp(phone: str, message: str):
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no  = phone,
            message   = message,
            wait_time = 30,   
            tab_close = True
        )
        time.sleep(5)  # Wait for message box to be ready
        pyautogui.press("enter")  # auto press Enter
        print(f"[✓] Sent to {phone}")
    except Exception as e:
        print(f"[!] Failed sending to {phone}: {e}")

def main():
    df = pd.read_excel(CSV_PATH)


    for _, row in df.iterrows():
        name   = str(row["name"]).strip()
        phone  = str(row["phone_number"]).strip()
        site   = sanitize_url(str(row["website"]).strip())

        print(f"\n➡️  Processing {name} | {phone} | {site}")

        snapshot   = scrape_website(site)
        prompt     = build_prompt(name, snapshot)
        message    = query_ollama(prompt)

        if not message:
            message = f"Hi {name}, I help businesses like yours grow using targeted digital marketing. Interested in a quick chat?"
            print("   Using fallback message (Ollama failed).")

        print(f"   Final message:\n   {message}\n")
        send_whatsapp(phone, message)

        time.sleep(WAIT_BETWEEN)

if __name__ == "__main__":
    main()