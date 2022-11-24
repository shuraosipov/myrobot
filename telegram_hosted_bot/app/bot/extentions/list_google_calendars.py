import logging
import requests
import json

from auth import check_auth_or_ask_for_login


@check_auth_or_ask_for_login
def calendar(update,context):
    logging.info("Displaying list of calendars")
    calendars = list_google_calendars(context.user_data.get("google_access_token"))
    text = "🗓 Your Google Calendars:\n\n"
    
    for calendar_name in calendars:
        text += f"* {calendar_name}\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def list_google_calendars(access_token) -> list:
    """Get List of calendars from Google Calendar API using the access token from the user."""
    URL = "https://www.googleapis.com/calendar/v3/users/me/calendarList"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:

        logging.info("Successfully retrieved calendars from Google Calendar API")
        calendars = []
        for calendar in json.loads(response.text)["items"]:
            if calendar["summary"] != "shuraosipov@gmail.com":
                calendars.append(calendar["summary"])
        return calendars
    else:
        logging.error(f"Failed to retrieve calendars from Google Calendar API. Error: {response.status_code}")
        return []