# Telegram Appointment Booking Bot

Automated Telegram appointment booking bot for service-based businesses.  
Collects client details, records appointments into SQLite and notifies the administrator in real time.

---

## ✨ Features

- **FSM-based conversation flow** – step-by-step data collection without free-form chaos.
- **Flexible contact capture** – supports both Telegram contact sharing and manual phone input.
- **Service selection keyboard** – easily configurable list of services.
- **Dynamic date keyboard** – shows the next 7 days.
- **Dynamic time keyboard**
  - hides past hours for the current day
  - hides already booked time slots (taken from SQLite database)
- **SQLite storage** – all applications are stored as records (e.g. with `pending` status).
- **Admin notification** – administrator receives a detailed message for each new booking.

---

## 🧱 Tech stack

- Python 3.x
- [python-telegram-bot 20.x](https://docs.python-telegram-bot.org/)
- SQLite (built-in)

---

## 🚀 How to run locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/dmytrothedev/telegram-appointment-bot.git
   cd telegram-appointment-bot

## Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows


## Install dependencies

pip install -r requirements.txt


## Configure the bot. Create a new file config.py in the project folder using config_example.py as a template:

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_ID = "YOUR_ADMIN_CHAT_ID"
python -m venv venv


## Run

python main.py

---

## 📂 Project structure

handlers/           # message & callback handlers
keyboards/          # dynamic keyboards: services, dates, time, contact
config_example.py   # configuration template (copy it to config.py locally)
db.py               # SQLite helper functions
main.py             # entry point and Telegram bot setup
requirements.txt    # dependencies
.gitignore          # ignored files and folders
README.md           # documentation


## 🔧 Customization

This bot can be tailored for different businesses:

Update working hours and time slots

Modify services list

Change admin notifications format

Export data into Google Sheets

Add admin tools (approve / reject bookings)

Add payment step or prepayment


## 💼 Use cases

Beauty salons & barbershops

Clinics and private specialists

Photo / tattoo / dance studios

Personal trainers and consultants

Repair services and mobile technicians


## ⭐ About the project

This bot was developed as a reusable appointment scheduling system.
Feel free to fork the repo, submit pull requests and open issues.


   
