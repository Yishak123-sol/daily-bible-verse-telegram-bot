import os
from datetime import datetime
from fastapi import FastAPI
from telegram import Bot
from bible_plan import bible_reading_plan
import requests
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID") 
bot = Bot(token=TOKEN)

START_DATE = datetime(2025, 5, 5)  

def get_verse_text(passage):
    response = requests.get(f"https://bible-api.com/{passage}")
    if response.status_code == 200:
        data = response.json()
        return data.get("text", "Verse not found")
    else:
        return "Error fetching verse."

def get_day_of_year():
    today = datetime.today().date()
    delta = today - START_DATE.date()
    return delta.days + 1 
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Bible bot is up."}

@app.post("/send")
async def send_daily_reading():
    day_of_year = get_day_of_year()
    readings = bible_reading_plan.get(str(day_of_year), [])

    if not readings:
        return {"status": "done", "message": f"No readings found for day {day_of_year}."}

    # Prepare the message to be sent
    message = f"\U0001F4D6 *Day {day_of_year} Bible Reading Plan*\n\n"
    for reading in readings:
        verse_text = get_verse_text(reading)
        message += f"*{reading}*\n{verse_text}\n\n"

    MAX_LENGTH = 4096  
    for i in range(0, len(message), MAX_LENGTH):
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=message[i:i + MAX_LENGTH],
            parse_mode="Markdown"
        )

    return {"status": "sent", "day": day_of_year, "readings": readings}













# import os
# from datetime import datetime
# from fastapi import FastAPI
# from telegram import Bot
# from dotenv import load_dotenv
# from bible_plan import bible_reading_plan




# import os
# import requests
# from datetime import datetime
# from fastapi import FastAPI, BackgroundTasks
# from telegram import Bot
# from bible_plan import bible_reading_plan


# load_dotenv()
# TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID") 
# # Load environment variables from .env


# app = FastAPI()

# bot = Bot(token=TOKEN)

# # Define the starting date (today is Day 1)
# # start_date = datetime.today().date()  # Today's date will be Day 1
# start_date = datetime(2025, 5, 5)

# # Function to fetch Bible verse text from bible-api.com
# def get_verse_text(passage: str):
#     response = requests.get(f"https://bible-api.com/{passage}")
#     if response.status_code == 200:
#         data = response.json()
#         return data.get("text", "Verse not found")
#     else:
#         return "Error fetching verse."

# # Function to calculate the number of days passed since the start date
# def get_day_of_year():
#     today = datetime.today().date()
#     delta = today - start_date
#     return delta.days + 1  # Start from 1 for Day 1

# # Function to send daily Bible reading plan
# async def send_daily_reading():
#     # Calculate the current day (starting from Day 1 today)
#     day_of_year = get_day_of_year()
    
#     # Get the Bible readings for the calculated day
#     readings = bible_reading_plan.get(str(day_of_year), [])
    
#     if not readings:
#         print(f"No readings found for day {day_of_year}.")
#         return

#     # Prepare the message to be sent
#     message = f"\U0001F4D6 *Day {day_of_year} Bible Reading Plan*\n\n"
#     for reading in readings:
#         verse_text = get_verse_text(reading)
#         message += f"*{reading}*\n{verse_text}\n\n"

#     # Split message if too long for Telegram
#     MAX_LENGTH = 4096
#     for i in range(0, len(message), MAX_LENGTH):
#         await bot.send_message(
#             chat_id=CHANNEL_ID,
#             text=message[i:i+MAX_LENGTH],
#             parse_mode='Markdown'
#         )

# # FastAPI app instance
# app = FastAPI()

# # Define the endpoint to trigger sending daily Bible reading
# @app.get("/")
# async def root():
#     return {"message": "Bible bot is up."}

# # Background task to send daily reading
# @app.get("/send-daily-reading")
# async def send_daily_reading_task(background_tasks: BackgroundTasks):
#     background_tasks.add_task(send_daily_reading)
#     return {"status": "Reading plan task is running."}

# # This can be scheduled using a cron job or another task scheduler to run daily
# @app.on_event("startup")
# async def startup_event():
#     # Here you could add a scheduler for sending the daily reading automatically if needed
#     # For example, using an external service to call the `/send-daily-reading` route at a specific time
#     pass
