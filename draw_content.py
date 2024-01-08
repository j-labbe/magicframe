import sys
from PIL import Image, ImageDraw, ImageFont
import datetime
# from waveshare_epd import epd7in5_V2

def draw_display(current_day, current_month, travel_time, travel_time_delay, current_temperature, forecast, quote, quote_author):

    ######################
    # Initialize display #
    ######################
    # display = epd7in5_V2.EPD()
    # display.init()

    background = Image.open('bg.jpg')
    background = background.resize((480, 800))
    draw = ImageDraw.Draw(background)

    ########################
    # Draw the card titles #
    ########################
    font = ImageFont.truetype('font/Roboto-Bold.ttf', size=14)
    draw.text((55, 282), "Travel Time", font=font, fill=(0, 0, 0))
    draw.text((285, 282), "Current Temperature", font=font, fill=(0, 0, 0))
    draw.text((55, 459), "Forecast", font=font, fill=(0, 0, 0))
    draw.text((55, 627), "Quote of the Day", font=font, fill=(0, 0, 0))

    ########################
    # Draw the date number #
    ########################
    font_big_bold = ImageFont.truetype('font/Roboto-Regular.ttf', size=112)

    # Center the date
    date_num_text = current_day

    # Calculate the text size
    date_num_text_width = draw.textlength(date_num_text, font=font_big_bold)

    # Calculate the x-coordinate to center the text horizontally
    date_num_text_x = (480 - date_num_text_width) // 2

    # Fixed y-coordinate for the text
    date_num_text_y = 50

    # Draw the centered text
    draw.text((date_num_text_x, date_num_text_y), date_num_text, font=font_big_bold, fill=(0, 0, 0))

    #######################
    # Draw cenetered line #
    #######################
    center_x1 = (480 - 150) // 2
    center_x2 = center_x1 + 150

    # Calculate the y-coordinate for the line
    line_y = 180

    # Draw a centered horizontal line
    line_color = (0, 0, 0)  # Black color
    line_width = 3

    draw.line([(center_x1, line_y), (center_x2, line_y)], fill=line_color, width=line_width)

    #######################
    # Draw the date month #
    #######################

    font_month = ImageFont.truetype('font/Roboto-Medium.ttf', size=20)

    # Center the date
    date_month_text = current_month.upper()

    # Calculate the text size
    date_month_text_width = draw.textlength(date_month_text, font=font_month)

    # Calculate the x-coordinate to center the text horizontally
    date_month_text_x = (480 - date_month_text_width) // 2

    # Fixed y-coordinate for the text
    date_month_text_y = 195

    # Draw the centered text
    draw.text((date_month_text_x, date_month_text_y), date_month_text, font=font_month, fill=(0, 0, 0))

    ##################################
    # Draw the Estimated Travel Time #
    ##################################

    card_large_font = ImageFont.truetype('font/Roboto-Medium.ttf', size=42)
    card_small_font = ImageFont.truetype('font/Roboto-Regular.ttf', size=18)
    card_medium_font = ImageFont.truetype('font/Roboto-Regular.ttf', size=16)

    first_text = str(travel_time)
    first_text_width = draw.textlength(first_text, font=card_large_font)

    # Calculate the starting x-coordinate for the second text
    x_second_text = 95 + first_text_width + 5  # Adjust the padding as needed

    # Draw the first text
    draw.text((95, 320), first_text, font=card_large_font, fill=(0, 0, 0))

    # Draw the second text to the right of the first text
    second_text = f"min{'s' if travel_time != 1 else ''}"
    draw.text((x_second_text, 337), second_text, font=card_small_font, fill=(128,128,128))

    draw.text((80, 385), f"{travel_time_delay} {second_text} delay", font=card_medium_font, fill=(0, 0, 0))

    ########################
    # Draw the Temperature #
    ########################

    card_small_font = ImageFont.truetype('font/Roboto-Regular.ttf', size=20)

    temp_text = str(current_temperature)
    temp_text_width = draw.textlength(temp_text, font=card_large_font)

    # Calculate the starting x-coordinate for the second text
    x_temp_second_text = 330 + temp_text_width + 5  # Adjust the padding as needed

    # Draw the first text
    draw.text((330, 320), temp_text, font=card_large_font, fill=(0, 0, 0))

    # Draw the second text to the right of the first text
    draw.text((x_temp_second_text, 323), "°F", font=card_small_font, fill=(128,128,128))


    ###########################
    # Draw the Forecast Lines #
    ###########################

    # Number of lines
    num_lines = 6

    # Coordinates
    start_x = 20
    end_x = 460
    start_y = 490
    end_y = 570

    spacing = (end_x - start_x) / (num_lines)

    weather_font = ImageFont.truetype('font/Roboto-Regular.ttf', size=12)

    for i in range(num_lines):
        x1 = start_x + i * spacing
        x2 = start_x + (i + 1) * spacing
        midpoint = (x1 + x2) / 2

        if i != 0:
            # Drawing the lines
            draw.line([(x1, start_y), (x1, end_y)], fill=(128, 128, 128), width=2)

        # This text is for the date
        forecast_date = datetime.datetime.fromisoformat(forecast[i]["date"]).strftime("%a")
        text = f"{forecast_date}"
        text_bbox = draw.textbbox((0, 0), text, font=weather_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = midpoint - text_width / 2
        text_y = 492
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=weather_font)

        icon = Image.open(f"icons/{forecast[i]['conditions']}.png")
        icon_resized = icon.resize((24, 24))
        background.paste(icon_resized, (int(midpoint - 12), 515), icon_resized)

        # This text is for the temperature
        text = f"{forecast[i]['temperature']}°"
        text_bbox = draw.textbbox((0, 0), text, font=weather_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_x = (midpoint - text_width / 2) + 2 # Shift 2 pixels right to offset the degree symbol
        text_y = 555
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=weather_font)

    ##################
    # Draw the Quote #
    ##################
     
    quote_font = ImageFont.truetype("font/Merriweather-Italic.ttf", size=16)
    author_font = ImageFont.truetype("font/Merriweather-Regular.ttf", size=14)
    wrapped_text, bottom_y = wrap_text(quote, quote_font, 400, draw, 660)
    draw.text((40, 660), f"\"{wrapped_text}\"", font=quote_font, fill=(0, 0, 0))
    draw.text((40, bottom_y + 15), f"- {quote_author}", font=author_font, fill=(85,85,85))


    ###########################
    # Save the modified image #
    ###########################
    background.save('last_render.png')
    # display.display(display.getbuffer(background))

    message = input("Press enter to quit")

    # display.Clear()

# display.update_display()
#message = input("Press enter to quit\n\n")
# display.clear_display()
#GPIO.cleanup()
    
def wrap_text(text, font, max_width, draw, start_y):
    """
    Wraps text and calculates the bottom of the text box.
    Args:
    text (str): The text to be wrapped.
    font (ImageFont): The font to be used.
    max_width (int): The maximum width in pixels for a line of text.
    draw (ImageDraw): The ImageDraw object used to render the text.
    start_y (int): The starting y-coordinate of the text.
    
    Returns:
    Tuple[str, int]: The wrapped text and the bottom y-coordinate of the text box.
    """
    lines = []
    total_height = 0

    words = text.split()
    while words:
        line = ''
        while words:
            test_line = line + words[0] + ' '
            # Check the width of the text using textbbox
            text_bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            if text_width > max_width:
                break
            line = test_line
            words.pop(0)

        # Calculate height of each line
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_height = line_bbox[3] - line_bbox[1]
        total_height += line_height

        lines.append(line.strip())

    bottom_y = start_y + total_height
    return '\n'.join(lines), bottom_y