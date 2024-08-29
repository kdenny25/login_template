from PIL import Image, ImageFont, ImageDraw
import io
import base64
import random


colors = {
    "green": ["#0D7C66", "#41B3A2"],
    "blue": ["#7C93C3", "#55679C"],
    "orange": ["#FABC3F", "#E85C0D"],
    "red": ["#C73659", "#A91D3A"]
}

def gen_image(name):
    """Generates a profile pic using the initials of the user and randomly assigns a color scheme"""
    W, H = (256,256)

    # create initials
    split_name = name.split()
    initials = ""
    for word in split_name[:2]:
        initials = initials + word[0]
    initials = initials.upper()

    # color selection
    rnum = random.randrange(0,3)
    colorscheme = colors[list(colors.keys())[rnum]]

    font = ImageFont.truetype(r'./utilities/Lato-Bold.ttf', size=150)
    #font = ImageFont.truetype(r'Lato-Bold.ttf', size=150)
    # generate a profile picture
    img = Image.new(mode="RGBA", size=(W, H), color=colorscheme[0])
    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), initials, font=font)
    draw.text(((W - w) / 2, (H - h) / 3), initials, fill=colorscheme[1], font=font)

    data = io.BytesIO()
    img.save(data, 'PNG')
    encoded_img_data = base64.b64encode(data.getvalue())


    return encoded_img_data




if __name__ == "__main__":
    gen_image("ronny donny")