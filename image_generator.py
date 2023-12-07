import csv
import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops

def sanitize_filename(filename):
    # Remove special characters and spaces, and replace them with underscores
    return re.sub(r'[^\w\s.-]', '_', filename)

def read_csv_file(file_path, encoding='utf-8'):
    names = []
    cities = []
    with open(file_path, 'r', newline='', encoding=encoding) as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) >= 2:
                names.append(row[0])
                cities.append(row[1])
            else:
                names.append('')
                cities.append('')
    return names, cities

def read_template_image(template_path):
    try:
        template_image = Image.open(template_path)
        return template_image
    except FileNotFoundError:
        print(f"Template image not found at '{template_path}'")
        return None

def apply_text_effects(draw, text, position, font, fill_color, stroke_color, stroke_width, bevel_emboss):
    if bevel_emboss:
        bevel_image = draw.text(position, text, fill=fill_color, font=font)

        if bevel_image:
            emboss_image = bevel_image.filter(ImageFilter.EMBOSS)
            draw.bitmap(position, emboss_image, fill=fill_color)

    if stroke_color:
        for dx in [-stroke_width, stroke_width]:
            for dy in [-stroke_width, stroke_width]:
                draw.text((position[0] + dx, position[1] + dy), text, font=font, fill=stroke_color)

def apply_drop_shadow(image, text, position, font, fill_color, shadow_color, shadow_offset):
    shadow_image = Image.new('RGBA', image.size)
    shadow_draw = ImageDraw.Draw(shadow_image)

    shadow_position = (position[0] + shadow_offset[0], position[1] + shadow_offset[1])

    shadow_draw.text(shadow_position, text, font=font, fill=shadow_color)
    shadow_image = shadow_image.filter(ImageFilter.GaussianBlur(radius=1))
    return Image.alpha_composite(image.convert('RGBA'), shadow_image)

def generate_and_save_images(names, cities, template_image, output_directory):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    for i in range(len(names)):
        if names[i] and cities[i]:
            # Create a copy of the template image
            image_with_text = template_image.copy()

            # Create a drawing context to add text
            draw = ImageDraw.Draw(image_with_text)

            # Define font size and Y position for both the name and city text
            font_size = 160  # Adjust the font size as needed
            y_position = 715  # You can adjust the Y position as needed
            y_position_city = 1200  # You can adjust the Y position as needed


            # Define font for both the name and city text
            font = ImageFont.truetype(font_location, font_size)


            # Determine the X position for the city text based on letter count
            city_x_position = (template_image.width - draw.textbbox((0, 0), cities[i], font=font)[2]) // 2
            

            # Determine the X position for the name text based on letter count (including spaces)
            name_x_position = name_x_position = (template_image.width - draw.textbbox((0, 0), names[i], font=font)[2]) // 2

            # Position for both the name and city text
            name_position = (name_x_position, y_position)
            city_position = (city_x_position, y_position_city)

            # Apply text effects for the name
            apply_text_effects(draw, names[i], name_position, font, "#000000", "#FFBE00", 2, bevel_emboss=True)


            # Apply drop shadow for the city
            image_with_text = apply_drop_shadow(image_with_text, cities[i], city_position, font, "#FFFFFF", "white", (5, 5))

            # Sanitize the filename to remove special characters
            sanitized_name = sanitize_filename(names[i])
            sanitized_city = sanitize_filename(cities[i])

            # Generate the sanitized output file path
            output_filename = f"{i+1}_{sanitized_name}_{sanitized_city}.jpg"
            output_path = os.path.join(output_directory, output_filename)

            # Convert the image to RGB mode before saving as JPEG
            image_with_text = image_with_text.convert('RGB')
            image_with_text.save(output_path)
            print(f"Saved image {i+1} to '{output_path}'")



def count_letters_in_name(name):
    # Remove any spaces and special characters from the name
    name = ''.join(filter(str.isalnum, name))
    
    # Count the number of letters in the cleaned name
    letter_count = len(name)
    
    return letter_count

os.system("color 0a")
	
print("""
   _____ _____   _____            _____                               _____                           _             
  / ____|  __ \ / ____|          |_   _|                             / ____|                         | |            
 | |    | |__) | |       ______    | |  _ __ ___   __ _  __ _  ___  | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
 | |    |  ___/| |      |______|   | | | '_ ` _ \ / _` |/ _` |/ _ \ | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |____| |    | |____            _| |_| | | | | | (_| | (_| |  __/ | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
  \_____|_|     \_____|          |_____|_| |_| |_|\__,_|\__, |\___|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                                                         __/ |                                                      
  ____                            _ _          _ _      |___/ _                                                     
 |  _ \                     /\   | (_)        (_) |     | |  | |                                                    
 | |_) |_   _   ______     /  \  | |_ ______ _ _| |__   | |__| | __ _ ___ ___  __ _ _ __                            
 |  _ <| | | | |______|   / /\ \ | | |_  / _` | | '_ \  |  __  |/ _` / __/ __|/ _` | '_ \                           
 | |_) | |_| |           / ____ \| | |/ / (_| | | |_) | | |  | | (_| \__ \__ \ (_| | | | |                          
 |____/ \__, |          /_/    \_\_|_/___\__,_|_|_.__/  |_|  |_|\__,_|___/___/\__,_|_| |_|                          
         __/ |                                                                                                      
        |___/ 
""")	
	
	
print("Starting ... \n")	
	
# Example usage:
csv_file_path = 'csv_input/all.csv'
template_image_path = 'base_image/template.jpg'
output_directory = 'output/'
font_location = 'font/Gobold Bold Italic.otf'

names, cities = read_csv_file(csv_file_path, encoding='ISO-8859-1')
template_image = read_template_image(template_image_path)


if template_image:
    generate_and_save_images(names, cities, template_image, output_directory)

	
	
print("Complete")
