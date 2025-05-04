import asyncio
import requests
import schedule
import time
from datetime import datetime
from telegram import Bot
from bible_plan import bible_reading_plan
from datetime import datetime, timedelta


import os
from telegram import Bot

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID")
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Define the starting date (today is Day 1)
start_date = datetime.today().date()  # Today's date will be Day 1

# Function to fetch Bible verse text from bible-api.com
def get_verse_text(passage):
    response = requests.get(f"https://bible-api.com/{passage}")
    if response.status_code == 200:
        data = response.json()
        return data.get("text", "Verse not found")
    else:
        return "Error fetching verse."

# Function to calculate the number of days passed since the start date
def get_day_of_year():
    today = datetime.today().date()
    delta = today - start_date
    return delta.days + 1  # Start from 1 for Day 1

# Function to send daily Bible reading plan
async def send_daily_reading():
    # Calculate the current day (starting from Day 1 today)
    day_of_year = get_day_of_year()
    
    # Get the Bible readings for the calculated day
    readings = bible_reading_plan.get(str(day_of_year), [])
    
    if not readings:
        print(f"No readings found for day {day_of_year}.")
        return

    # Prepare the message to be sent
    message = f"\U0001F4D6 *Day {day_of_year} Bible Reading Plan*\n\n"
    for reading in readings:
        verse_text = get_verse_text(reading)
        message += f"*{reading}*\n{verse_text}\n\n"

    # Split message if too long for Telegram
    MAX_LENGTH = 4096
    for i in range(0, len(message), MAX_LENGTH):
        await bot.send_message(
            chat_id=TELEGRAM_CHANNEL_ID,
            text=message[i:i+MAX_LENGTH],
            parse_mode='Markdown'
        )

# Function to run the scheduled task
def run_async_job():
    asyncio.run(send_daily_reading())

# Get the current time
# current_time = datetime.now()
# test_time = current_time + timedelta(minutes=1)
# now = test_time.strftime("%H:%M")
# schedule.every().day.at(now).do(run_async_job)  

# Schedule to run at the adjusted time
schedule.every().day.at("05:00").do(run_async_job) 

print("Bot is running. Waiting for scheduled time...")
while True:
    schedule.run_pending()
    time.sleep(60)
