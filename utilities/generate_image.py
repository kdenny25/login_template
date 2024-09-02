from PIL import Image, ImageFont, ImageDraw
import io
import base64
import random


colors = {
    "green": [[(0, 146, 69), (252, 238, 33)], "#0D7C66", "#41B3A2"],
    "blue": [[(46, 49, 146), (27, 255, 255)], "#7C93C3", "#55679C"],
    "orange": [[(212, 20, 90), (251, 176, 59)], "#FABC3F", "#E85C0D"],
    "red": [[(255, 81, 47), (221, 36, 118)], "#9C3163", "#A91D3A"]
}
def interpolate(f_co, t_co, interval):
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

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
    rnum = random.randrange(0,4)
    colorscheme = colors[list(colors.keys())[rnum]]

    font = ImageFont.truetype(r'./utilities/Lato-Bold.ttf', size=150)
    #font = ImageFont.truetype(r'Lato-Bold.ttf', size=150)
    # generate a profile picture
    img = Image.new(mode="RGBA", size=(W, H), color=0)
    draw = ImageDraw.Draw(img)
    # create gradient
    for i, color in enumerate(interpolate(colorscheme[0][0], colorscheme[0][1], W * 2)):
        draw.line([(0, i), (W, i)], tuple(color), width=1)

    _, _, w, h = draw.textbbox((0, 0), initials, font=font)
    draw.text(((W - w) / 2, (H - h) / 3), initials, fill=colorscheme[1], font=font)

    data = io.BytesIO()
    img.save(data, 'PNG')
    print(type(data.getvalue()))
    encoded_img_data = base64.b64encode(data.getvalue())
    print(type(encoded_img_data))
    img.show()
    return encoded_img_data




if __name__ == "__main__":
    gen_image("ronny donny")