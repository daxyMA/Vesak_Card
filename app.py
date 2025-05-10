from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate_image", methods=["GET"])
def generate_image():
    to_name = request.args.get("to", "Friend")
    from_name = request.args.get("from", "Me")

    base = Image.open("static/card_base.png").convert("RGBA")
    draw = ImageDraw.Draw(base)
    font = ImageFont.truetype("fonts/BebasNeue-Regular.ttf", size=50)

    image_width, image_height = base.size

    # TO
    label_to = "To:"
    name_to = to_name
    label_to_width = draw.textlength(label_to, font=font)
    name_to_width = draw.textlength(name_to, font=font)
    total_to_width = label_to_width + name_to_width + 20

    to_x = (image_width - total_to_width) // 2
    to_y = image_height - 200
    draw.text((to_x, to_y), label_to, font=font, fill="white")
    draw.text((to_x + label_to_width + 20, to_y), name_to, font=font, fill="yellow")

    # FROM
    label_from = "From:"
    name_from = from_name
    label_from_width = draw.textlength(label_from, font=font)
    name_from_width = draw.textlength(name_from, font=font)
    total_from_width = label_from_width + name_from_width + 20

    from_x = (image_width - total_from_width) // 2
    from_y = image_height - 130
    draw.text((from_x, from_y), label_from, font=font, fill="white")
    draw.text((from_x + label_from_width + 20, from_y), name_from, font=font, fill="yellow")

    # Output
    img_io = BytesIO()
    base.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
