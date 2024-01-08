import logging
from dotenv import load_dotenv
from create_content import ContentCreator
from draw_content import draw_display

def main():
    load_dotenv()
    logging.info("Creating content...")
    content = ContentCreator().create_content()
    logging.info("Displaying content...")

    current_day = content["date"]["current_day"]
    current_month = content["date"]["current_month"]

    travel_time = content["travel"]["time"]
    travel_time_delay = content["travel"]["delay"]

    current_temperature = content["weather"][0]["temperature"]
    forecast = content["weather"][1:]

    quote, author = content["quote"]


    draw_display(
        current_day=current_day,
        current_month=current_month,
        travel_time=travel_time,
        travel_time_delay=travel_time_delay,
        current_temperature=current_temperature,
        forecast=forecast,
        quote=quote,
        quote_author=author
    )

if __name__ == "__main__":
    main()
