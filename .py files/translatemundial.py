import tkinter as tk
from tkinter import ttk
import pyautogui
import pytesseract
import os
from PIL import Image
from deep_translator import GoogleTranslator
from pynput import mouse


# ruta de tesseract, hay que descargarlo e instalarlo, *RUTA GENERICA*
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Códigos de Tesseract y Google Translator
language_data = [
    ('Afrikaans', 'af', 'afr'),
    ('Albanian', 'sq', 'sq'),
    ('Amharic', 'am', 'amh'),
    ('Arabic', 'ar', 'ara'),
    ('Armenian', 'hy', 'hye'),
    ('Assamese', 'as', 'asm'),
    ('Azerbaijani', 'az', 'aze'),
    ('Basque', 'eu', 'eus'),
    ('Belarusian', 'be', 'bel'),
    ('Bengali', 'bn', 'ben'),
    ('Bosnian', 'bs', 'bos'),
    ('Bulgarian', 'bg', 'bul'),
    ('Catalan; Valencian', 'ca', 'cat'),
    ('Chinese (Simplified)', 'zh-CN', 'chi_sim'),
    ('Chinese (Traditional)', 'zh-TW', 'chi_tra'),
    ('Croatian', 'hr', 'hrv'),
    ('Czech', 'cs', 'ces'),
    ('Danish', 'da', 'dan'),
    ('Dutch', 'nl', 'nld'),
    ('English', 'en', 'eng'),
    ('Esperanto', 'eo', 'epo'),
    ('Estonian', 'et', 'est'),
    ('Finnish', 'fi', 'fin'),
    ('French', 'fr', 'fra'),
    ('Galician', 'gl', 'glg'),
    ('Georgian', 'ka', 'kat'),
    ('German', 'de', 'deu'),
    ('Greek', 'el', 'ell'),
    ('Gujarati', 'gu', 'guj'),
    ('Haitian Creole', 'ht', 'hat'),
    ('Hebrew', 'he', 'heb'),
    ('Hindi', 'hi', 'hin'),
    ('Hungarian', 'hu', 'hun'),
    ('Icelandic', 'is', 'isl'),
    ('Indonesian', 'id', 'ind'),
    ('Irish', 'ga', 'gle'),
    ('Italian', 'it', 'ita'),
    ('Japanese', 'ja', 'jpn'),
    ('Javanese', 'jw', 'jav'),
    ('Kannada', 'kn', 'kan'),
    ('Kazakh', 'kk', 'kaz'),
    ('Khmer', 'km', 'khm'),
    ('Korean', 'ko', 'kor'),
    ('Kurdish (Kurmanji)', 'ku', 'kur'),
    ('Kyrgyz', 'ky', 'kir'),
    ('Lao', 'lo', 'lao'),
    ('Latin', 'la', 'lat'),
    ('Latvian', 'lv', 'lav'),
    ('Lithuanian', 'lt', 'lit'),
    ('Luxembourgish', 'lb', 'ltz'),
    ('Macedonian', 'mk', 'mkd'),
    ('Malay', 'ms', 'msa'),
    ('Malayalam', 'ml', 'mal'),
    ('Maltese', 'mt', 'mlt'),
    ('Maori', 'mi', 'mri'),
    ('Marathi', 'mr', 'mar'),
    ('Mongolian', 'mn', 'mon'),
    ('Nepali', 'ne', 'nep'),
    ('Norwegian', 'no', 'nor'),
    ('Persian', 'fa', 'fas'),
    ('Polish', 'pl', 'pol'),
    ('Portuguese', 'pt', 'por'),
    ('Punjabi', 'pa', 'pan'),
    ('Quechua', 'qu', 'que'),
    ('Romanian', 'ro', 'ron'),
    ('Russian', 'ru', 'rus'),
    ('Scottish Gaelic', 'gd', 'gla'),
    ('Serbian', 'sr', 'srp'),
    ('Sindhi', 'sd', 'snd'),
    ('Sinhala', 'si', 'sin'),
    ('Slovak', 'sk', 'slk'),
    ('Slovenian', 'sl', 'slv'),
    ('Somali', 'so', 'som'),
    ('Spanish', 'es', 'spa'),
    ('Swahili', 'sw', 'swa'),
    ('Swedish', 'sv', 'swe'),
    ('Tagalog (Filipino)', 'tl', 'tgl'),
    ('Tajik', 'tg', 'tgk'),
    ('Tamil', 'ta', 'tam'),
    ('Tatar', 'tt', 'tat'),
    ('Telugu', 'te', 'tel'),
    ('Thai', 'th', 'tha'),
    ('Tibetan', 'bo', 'bod'),
    ('Tigrinya', 'ti', 'tir'),
    ('Tonga', 'to', 'ton'),
    ('Turkish', 'tr', 'tur'),
    ('Ukrainian', 'uk', 'ukr'),
    ('Urdu', 'ur', 'urd'),
    ('Uzbek', 'uz', 'uzb'),
    ('Vietnamese', 'vi', 'vie'),
    ('Welsh', 'cy', 'cym'),
    ('Xhosa', 'xh', 'xho'),
    ('Yiddish', 'yi', 'yid'),
    ('Yoruba', 'yo', 'yor'),
    ('Zulu', 'zu', 'zul')
]
# OJO!! Solo se puede de arriba a la izquierda, hacia abajo derecha 
class ScreenCapture:
    def __init__(self):
        self.start_pos = None
        self.end_pos = None

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.start_pos = (x, y)
            print(f"Inicio en: {self.start_pos}")
        else:
            self.end_pos = (x, y)
            print(f"Fin en: {self.end_pos}")
            return False

    def capture_region(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            print("Haz clic y arrastra para seleccionar la región. Suelta el clic para capturar.")
            listener.join()

        if self.start_pos and self.end_pos:
            x1, y1 = self.start_pos
            x2, y2 = self.end_pos
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            width = x2 - x1
            height = y2 - y1
            region = (x1, y1, width, height)
            return region
        else:
            return None

def ocr_and_translate(region, lang_index):
    if region:
        screenshot = pyautogui.screenshot(region=region)
        # Imagen temp, ¿cambiar de ruta?
        temp_img_path = "temp.png"
        screenshot.save(temp_img_path)
        tesseract_lang_code = language_data[lang_index][2]
        ocr_result = pytesseract.image_to_string(Image.open(temp_img_path), lang=tesseract_lang_code)
        print(f"Texto reconocido:\n{ocr_result}")
        
        # Traducir
        google_source_lang_code = language_data[lang_index][0].lower() 
        target_lang = 'es' 
        translation = GoogleTranslator(source=google_source_lang_code, target=target_lang).translate(ocr_result)
        print(f"Traducción a {target_lang}:\n{translation}")
        # Eliminar la imagen temporal
        os.remove(temp_img_path)
    else:
        print("No se ha especificado una región válida.")

def start_capture(lang_index):
    screen_capture = ScreenCapture()
    region = screen_capture.capture_region()

    if region:
        ocr_and_translate(region, lang_index)
    else:
        print("No se pudo capturar la región correctamente.")

def on_language_selected(event):
    selected_lang = language_combobox.get()
    lang_index = next((i for i, lang_data in enumerate(language_data) if lang_data[0] == selected_lang), None)
    if lang_index is not None:
        start_capture(lang_index)
    else:
        print("No se encontró el idioma seleccionado en los datos.")

root = tk.Tk()
root.title("OCR y Traducción")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

language_label = ttk.Label(frame, text="Selecciona el idioma:")
language_label.grid(row=0, column=0, padx=10, pady=10)

language_names = [lang[0] for lang in language_data]
language_combobox = ttk.Combobox(frame, values=language_names, state="readonly", width=50)
language_combobox.grid(row=0, column=1, padx=10, pady=10)
language_combobox.current(0)

start_button = ttk.Button(frame, text="Comenzar Captura", command=lambda: on_language_selected(None))
start_button.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()
