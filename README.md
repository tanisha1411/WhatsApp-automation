# 🤖 WhatsApp Automated AI Message Generator

This tool automates personalized WhatsApp messaging at scale by combining the power of:

- 🧠 **LLMs (via Ollama)** for crafting human-like messages
- 🌐 **Website scraping** for contextual personalization
- 💬 **WhatsApp Web** (via `pywhatkit`) for message delivery
- 💬 **WhatsApp Automation** (via `pyautogui`) for automation

---

## 🚀 Features

- Reads contact info from a CSV/Excel (name, phone number, website)
- Scrapes each website for relevant content (title + text)
- Uses a local LLM (e.g. `mistral`, `llama3`) via Ollama to generate personalized messages
- Sends each message using WhatsApp Web automatically.
- Easy to customize, private, and 100% local

---

## 📁 CSV/Excel Format

Create a file called `contacts.csv` with the following headers:

```csv
name,phone_number,website
Alice,+911234567890,https://aliceshop.com
Bob,+971501234567,http://bobsdeals.in
