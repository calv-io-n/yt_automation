from PIL import Image, ImageDraw, ImageDraw

def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def rounded_rectangle(source):
    im = Image.open(source)

    # Create a drawing object
    draw = ImageDraw.Draw(im)

    # Draw a rounded rectangle on the image with a corner radius of 50 pixels
    draw.rounded_rectangle((0, 0, im.size[0], im.size[1]), 50, outline=(255, 255, 255), width=20)

    return im

def clip_img_format(source, rad=50):
    image = rounded_rectangle(source)
    image = add_corners(image, rad)
    return image

if __name__ == "__main__":
    test = rounded_rectangle("start.PNG")
    test = add_corners(test, 50)
    test.save("test.png")
