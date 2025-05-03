import json
import pygame

cores = {"vermelho": (255, 0, 0), "amarelo": (255, 255, 0), "azul": (0, 0, 255), "verde": (0, 128, 0), "preto": (0, 0, 0)}

window_sizes = [
    (800, 600),
    (1024, 768),
    (1280, 720),
    (1920, 1080)
]

BUTTON_WIDTH = 400
BUTTON_HEIGHT = 50
BUTTON_SPACING = 10
BUTTON_COLOR = (255, 255, 255)
BUTTON_ACTIVE_COLOR = (0, 0, 0)

WINDOW_TITLE = "Ticket to Ride"

BACKGROUND_IMAGE_PATH = "assets/settingsBG.jpg"

def save_config_to_json(filename):
    config = {
        "window_sizes": window_sizes,
        "button_width": BUTTON_WIDTH,
        "button_height": BUTTON_HEIGHT,
        "button_spacing": BUTTON_SPACING,
        "button_color": BUTTON_COLOR,
        "button_active_color": BUTTON_ACTIVE_COLOR,
        "window_title": WINDOW_TITLE,
        "background_image_path": BACKGROUND_IMAGE_PATH
    }
    
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)

def load_config_from_json(filename):
    global window_sizes, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_SPACING
    global BUTTON_COLOR, BUTTON_ACTIVE_COLOR, WINDOW_TITLE, BACKGROUND_IMAGE_PATH
    
    try:
        with open(filename, "r") as f:
            config = json.load(f)
        
        window_sizes = config.get("window_sizes", window_sizes)
        BUTTON_WIDTH = config.get("button_width", BUTTON_WIDTH)
        BUTTON_HEIGHT = config.get("button_height", BUTTON_HEIGHT)
        BUTTON_SPACING = config.get("button_spacing", BUTTON_SPACING)
        BUTTON_COLOR = tuple(config.get("button_color", BUTTON_COLOR))
        BUTTON_ACTIVE_COLOR = tuple(config.get("button_active_color", BUTTON_ACTIVE_COLOR))
        WINDOW_TITLE = config.get("window_title", WINDOW_TITLE)
        BACKGROUND_IMAGE_PATH = config.get("background_image_path", BACKGROUND_IMAGE_PATH)
    
    except FileNotFoundError:
        print("Arquivo de configurações não encontrado, usando configurações padrão.")

save_config_to_json("settings.json")

load_config_from_json("settings.json")
print(window_sizes, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_ACTIVE_COLOR)
