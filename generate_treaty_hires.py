
import os
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "Pictures", "treaty_parchment_blank_center.png")
OUTPUT_PATH = os.path.join(BASE_DIR, "Pictures", "treaty_replica_hires.png")
FONT_URL = "https://github.com/google/fonts/raw/main/ofl/pinyonscript/PinyonScript-Regular.ttf"
FONT_PATH = os.path.join(BASE_DIR, "PinyonScript-Regular.ttf")

# 1. Download Font
if not os.path.exists(FONT_PATH):
    print(f"Downloading font from {FONT_URL}...")
    try:
        response = requests.get(FONT_URL)
        response.raise_for_status()
        with open(FONT_PATH, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Failed to download font: {e}")
        FONT_PATH = None

# 2. Text Content (Full text)
title = "Articles of Pacification (1738)"
preamble = "In the name of God, Amen. Whereas Captain Cudjoe, Captain Accompong, Captain Johnny, Captain Cuffee, Captain Quaco, and several other negroes, their dependants and adherents, have been in a state of war and hostility, for several years past, against our sovereign Lord the King, and the inhabitants of this island; and whereas peace and friendship among mankind, and the preventing the effusion of blood, is agreeable to God, consonant to reason, and desired by every good man; and whereas his majesty George the Second, king of Great Britain, France, and Ireland, and of Jamaica, Lord, Defender of the Faith, etc. has, by his letters patent, dated February the twenty-fourth, one thousand seven hundred and thirty-eight, in the twelfth year of his reign, granted full power and authority to John Guthrie and Francis Sadler, esquires, to negotiate and finally conclude a treaty of peace and friendship with the aforesaid Captain Cudjoe, and the rest of his captains, adherents, and other his men; they mutually, sincerely, and amicably, have agreed to the following articles:"

articles = [
    "First, That all hostilities shall cease on both sides for ever.",
    "Second, That the said Captain Cudjoe, the rest of his captains, adherents, and men, shall be for ever hereafter in a perfect state of freedom and liberty, excepting those who have been taken by them, within two years last past, if such are willing to return to their said masters and owners, with full pardon and indemnity from their said masters or owners for what is past; provided always, that, if they are not willing to return, they shall remain in subjection to Captain Cudjoe and in friendship with us, according to the form and tenor of this treaty.",
    "Third, That they shall enjoy and possess, for themselves and posterity for ever, all the lands situate and lying between Trelawney Town and the Cockpits, to the amount of fifteen hundred acres, bearing north-west from the said Trelawny Town.",
    "Fourth, That they shall have liberty to plant the said lands with coffee, cocoa, ginger, tobacco, and cotton, and to breed cattle, hogs, goats, or any other stock, and dispose of the produce or increase of the said commodities to the inhabitants of this island; provided always, that when they bring the said commodities to market, they shall apply first to the custos, or any other magistrate of the respective parishes where they expose their goods to sale, for a licence to vend the same.",
    "Fifth, That Captain Cudjoe, and all the Captain's adherents, and people now in subjection to him, shall all live together within the bounds of Trelawny Town, and that they have liberty to hunt where they shall think fit, except within three miles of any settlement, crawl, or pen; provided always, that in case the hunters of Captain Cudjoe, and those of other settlements meet, then the hogs to be equally divided between both parties.",
    "Sixth, That the said Captain Cudjoe, and his successors, do use their best endeavours to take, kill, suppress, or destroy, either by themselves, or jointly with any other number of men, commanded on that service by his excellency the Governor, or commander in chief for the time being, all rebels wheresoever they be, throughout this island, unless they submit to the same terms of accommodation granted to Captain Cudjoe, and his successors.",
    "Seventh, That in case this island be invaded by any foreign enemy, the said Captain Cudjoe, and his successors hereinafter named or to be appointed, shall then, upon notice given, immediately repair to any place the Governor for the time being shall appoint, in order to repel the said invaders with his or their utmost force, and to submit to the orders of the commander in chief on that occasion.",
    "Eighth, That if any white man shall do any manner of injury to Captain Cudjoe, his successors, or any of his or their people, they shall apply to any commanding officer or magistrate in the neighbourhood for justice; and in case Captain Cudjoe, or any of his people, shall do any injury to any white person, he shall submit himself, or deliver up such offender to justice.",
    "Ninth, That if any negroes shall hereafter run away from their masters or owners, and shall fall into Captain Cudjoe's hands, they shall immediately be sent back to the chief magistrate of the next parish where they are taken; and those that bring them are to be satisfied for their trouble, as the legislature shall appoint.",
    "Tenth, That all negroes taken, since the raising of this party by Captain Cudjoe's people, shall immediately be returned.",
    "Eleventh, That Captain Cudjoe, and his successors, shall wait on his Excellency, or the commander in chief for the time being, every year, if thereunto required.",
    "Twelfth, That Captain Cudjoe, during his life, and the Captains succeeding him, shall have full power to inflict any punishment they think proper for crimes committed by their men among themselves, death only excepted; in which case, if the Captain thinks they deserve death, he shall be obliged to bring them before any justice of the peace, who shall order proceedings on their trial equal to those of other free Negroes.",
    "Thirteenth, That Captain Cudjoe, with his people, shall cut, clear, and keep open, large and convenient roads from Trelawny town to Westmorland and St. James's, and if possible, to St. Elizabeth's.",
    "Fourteenth, That two white men, to be nominated by his Excellency, or the commander in chief for the time being, shall constantly live and reside with Captain Cudjoe, and his successors, in order to maintain a friendly correspondence with the inhabitants of this island.",
    "Fifteenth, That Captain Cudjoe shall, during his life, be chief commander in Trelawny town; after his decease the command to devolve on his brother Captain Accompong; and in case of his decease, on his next brother Captain Johnny; and, failing him, Captain Cuffee shall succeed; who is to be succeeded by Captain Quaco; and after all their demises, the Governor, or Commander in Chief for the time being, shall appoint, from time to time, whom he thinks fit for that command."
]

footer = "Mark of Cudjoe X\nMarch 1, 1738"

# 3. Image Generation
def create_hires_image():
    try:
        # Load small parchment
        original = Image.open(IMAGE_PATH).convert("RGBA")
        
        # Scale UP to High Res (1200x1600) for sharp text
        target_size = (1200, 1600)
        img = original.resize(target_size, Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Fonts (Scaled up for 1200 width)
        if FONT_PATH:
            font_title = ImageFont.truetype(FONT_PATH, 42)
            font_text = ImageFont.truetype(FONT_PATH, 16)
            font_bold = ImageFont.truetype(FONT_PATH, 18) # Slightly larger for emphasis
        else:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()
            font_bold = ImageFont.load_default()

        # Margins & Layout
        margin_x = 90
        margin_y = 120
        max_width = width - (margin_x * 2)

        current_y = margin_y

        # Title
        bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = bbox[2] - bbox[0]
        draw.text(((width - title_w) / 2, current_y), title, font=font_title, fill="#2b1d0e")
        current_y += 60

        # Preamble
        preamble_lines = textwrap.wrap(preamble, width=110)
        for line in preamble_lines:
            bbox = draw.textbbox((0, 0), line, font=font_text)
            w = bbox[2] - bbox[0]
            draw.text(((width - w) / 2, current_y), line, font=font_text, fill="#2b1d0e")
            current_y += 24
        
        current_y += 30

        # 2 Columns for Articles
        col_gap = 60
        col_width = (max_width - col_gap) // 2
        col1_x = margin_x
        col2_x = margin_x + col_width + col_gap
        
        # Split articles approx half
        split_idx = 7
        col1_articles = articles[:split_idx]
        col2_articles = articles[split_idx:]
        
        y_col1 = current_y
        char_limit = 55 # Tuning for font size 16

        for article in col1_articles:
            wrapper = textwrap.TextWrapper(width=char_limit)
            lines = wrapper.wrap(article)
            for i, line in enumerate(lines):
                 f = font_bold if i == 0 and ("First," in line or "Second," in line) else font_text
                 draw.text((col1_x, y_col1), line, font=f, fill="#2b1d0e")
                 y_col1 += 22
            y_col1 += 12

        y_col2 = current_y
        for article in col2_articles:
            wrapper = textwrap.TextWrapper(width=char_limit)
            lines = wrapper.wrap(article)
            for line in lines:
                 draw.text((col2_x, y_col2), line, font=font_text, fill="#2b1d0e")
                 y_col2 += 22
            y_col2 += 12

        # Footer
        final_y = max(y_col1, y_col2) + 40
        draw.text((width - 300, final_y), footer, font=font_text, fill="#2b1d0e")

        # Save as NEW filename
        img.save(OUTPUT_PATH, "PNG")
        print(f"Success! High-res image saved to {OUTPUT_PATH}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_hires_image()
