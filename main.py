import json
import random
import uuid
import segno
import svgutils.transform
import svgwrite
import math
from segno import helpers
from svgutils.compose import Figure, SVG

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Use seed from config if available, otherwise generate a new one
seed = config.get("seed", str(uuid.uuid4()))
random.seed(seed)

def create_3d_cube(svgdrawer, insert, size=50, fill_color="#D1E2F2", stroke_color="#4365E1", x_angle=0, y_angle=0, z_angle=0, fill_opacity=1.0, stroke_opacity=1.0, face_scale=0.9, gap=20):
    rad = math.radians(0)
    x_rad = math.radians(x_angle)
    y_rad = math.radians(y_angle)
    z_rad = math.radians(z_angle)

    points = [
        (insert[0], insert[1]),
        (insert[0] + size * math.cos(rad), insert[1] + size * math.sin(rad)),
        (insert[0] + size * math.cos(rad) - size * math.sin(rad), insert[1] + size * math.sin(rad) + size * math.cos(rad)),
        (insert[0] - size * math.sin(rad), insert[1] + size * math.cos(rad))
    ]

    center = (insert[0] + size / 2, insert[1] + size / 2)

    def rotate_x(point, angle):
        x, y = point
        x -= center[0]
        y -= center[1]
        y_rot = y * math.cos(angle) - size * math.sin(angle)
        return (x + center[0], y_rot + center[1])

    def rotate_y(point, angle):
        x, y = point
        x -= center[0]
        y -= center[1]
        x_rot = x * math.cos(angle) + size * math.sin(angle)
        return (x_rot + center[0], y + center[1])

    def rotate_z(point, angle):
        x, y = point
        x -= center[0]
        y -= center[1]
        x_rot = x * math.cos(angle) - y * math.sin(angle)
        y_rot = x * math.sin(angle) + y * math.cos(angle)
        return (x_rot + center[0], y_rot + center[1])

    points = [rotate_x(p, x_rad) for p in points]
    points = [rotate_y(p, y_rad) for p in points]
    points = [rotate_z(p, z_rad) for p in points]

    def scale_point(point, scale):
        x, y = point
        x = center[0] + (x - center[0]) * scale
        y = center[1] + (y - center[1]) * scale
        return (x, y)

    scaled_points = [scale_point(p, face_scale) for p in points]

    def adjust_for_gap(point, direction, gap):
        x, y = point
        if direction == 'right':
            x += gap
        elif direction == 'left':
            x -= gap
        elif direction == 'up':
            y -= gap
        elif direction == 'down':
            y += gap
        return (x, y)

    front_face = [
        adjust_for_gap(scaled_points[0], 'down', gap),
        adjust_for_gap(scaled_points[1], 'down', gap),
        adjust_for_gap((scaled_points[1][0], scaled_points[1][1] + size * face_scale), 'down', gap),
        adjust_for_gap((scaled_points[0][0], scaled_points[0][1] + size * face_scale), 'down', gap)
    ]
    svgdrawer.add(svgdrawer.polygon(front_face, fill=fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

    top_face = [
        adjust_for_gap(scaled_points[0], 'up', gap),
        adjust_for_gap(scaled_points[1], 'up', gap),
        adjust_for_gap(scaled_points[2], 'up', gap),
        adjust_for_gap(scaled_points[3], 'up', gap)
    ]
    svgdrawer.add(svgdrawer.polygon(top_face, fill=fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

    side_face = [
        adjust_for_gap(scaled_points[1], 'right', gap),
        adjust_for_gap(scaled_points[2], 'right', gap),
        adjust_for_gap((scaled_points[2][0], scaled_points[2][1] + size * face_scale), 'right', gap),
        adjust_for_gap((scaled_points[1][0], scaled_points[1][1] + size * face_scale), 'right', gap)
    ]
    darker_fill_color = "#4365E1"
    svgdrawer.add(svgdrawer.polygon(side_face, fill=darker_fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

    bottom_face = [
        adjust_for_gap((scaled_points[0][0], scaled_points[0][1] + size * face_scale), 'down', gap),
        adjust_for_gap((scaled_points[1][0], scaled_points[1][1] + size * face_scale), 'down', gap),
        adjust_for_gap((scaled_points[2][0], scaled_points[2][1] + size * face_scale), 'down', gap),
        adjust_for_gap((scaled_points[3][0], scaled_points[3][1] + size * face_scale), 'down', gap)
    ]
    svgdrawer.add(svgdrawer.polygon(bottom_face, fill=fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

    back_face = [
        adjust_for_gap(scaled_points[3], 'left', gap),
        adjust_for_gap(scaled_points[2], 'left', gap),
        adjust_for_gap((scaled_points[2][0], scaled_points[2][1] + size * face_scale), 'left', gap),
        adjust_for_gap((scaled_points[3][0], scaled_points[3][1] + size * face_scale), 'left', gap)
    ]
    svgdrawer.add(svgdrawer.polygon(back_face, fill=fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

    left_face = [
        adjust_for_gap(scaled_points[0], 'left', gap),
        adjust_for_gap(scaled_points[3], 'left', gap),
        adjust_for_gap((scaled_points[3][0], scaled_points[3][1] + size * face_scale), 'left', gap),
        adjust_for_gap((scaled_points[0][0], scaled_points[0][1] + size * face_scale), 'left', gap)
    ]
    svgdrawer.add(svgdrawer.polygon(left_face, fill=fill_color, stroke=stroke_color, fill_opacity=fill_opacity, stroke_opacity=stroke_opacity))

def create_protein_chain(drawer, start_insert, num_cubes, size_increment=5, x_angle=0, y_angle=0, z_angle=0, size=20, phase_shift=0, gap=10):
    insert = start_insert
    for i in range(num_cubes):
        if random.choice([True, False]):
            fill_opacity = 1.0
            #fill_opacity = random.randrange(0, 100) / 100
            create_3d_cube(drawer, insert, size=size, x_angle=x_angle, y_angle=y_angle, z_angle=z_angle + phase_shift,
                           fill_opacity=fill_opacity,
                           stroke_opacity=fill_opacity, gap=gap, fill_color="white")
            insert = (insert[0] - size * 1.5, insert[1] - size * 0)
            size += size_increment
            x_angle += 5
            y_angle += 0
            z_angle += 50

def make_colored_qr_code(name="", phone="", email="", url="", filename="colored_qr_code.svg", fill_color="black", back_color="white"):
    qr = helpers.make_mecard(
        name=name, email=email, url=url, phone=phone)
    qr.save(filename, scale=10, data_dark=fill_color, dark=fill_color, light=back_color, border=1)

def create_fading_grid(dwg, start_insert, width, height, square_size=10, spacing=5, max_opacity=1.0):
    num_cols = int(width // (square_size + spacing))
    num_rows = int(height // (square_size + spacing))
    for row in range(num_rows):
        for col in range(num_cols):
            if random.choice([True, False]):
                x = start_insert[0] - col * (square_size + spacing)
                y = start_insert[1] - row * (square_size + spacing)
                opacity = max_opacity * (1 - (col + row) / (num_cols + num_rows))
                dwg.add(
                    dwg.rect(
                        insert=(x, y), size=(square_size, square_size),
                        fill="white", stroke="none", rx=1, ry=1, fill_opacity=opacity, stroke_opacity=opacity))

def back_qr_code(url = "https://github.com/noatgnu/business-card-generator"):
    qr = segno.make(url)
    qr.save("qr_code_back.svg", scale=10, data_dark=fill_color, dark=fill_color, light=back_color, border=1)


if __name__ == "__main__":
    version = "v1.0"
    width_mm = 84
    height_mm = 54

    width_px = width_mm * 3.5433
    height_px = height_mm * 3.5433

    dwg = svgwrite.Drawing("business_card.svg", size=(f"{width_px}px", f"{height_px}px"))

    border_width = config["border_width"]
    fill_color = config["fill_color"]
    back_color = config["back_color"]

    dwg.add(dwg.rect(insert=(0, 0), size=(width_px, height_px),
                     fill=fill_color, stroke=fill_color, stroke_width=border_width))

    dwg.add(dwg.rect(rx=0, ry=0,
                     insert=(border_width, border_width),
                     size=(width_px - 2 * border_width, height_px - 2 * border_width),
                     fill=fill_color, stroke="white"))

    create_fading_grid(dwg, start_insert=(width_px - width_px*0.05, height_px - height_px*0.075), width=width_px*2.1 // 4, height=height_px // 1.5,
                       square_size=5, spacing=5, max_opacity=0.5)

    create_protein_chain(dwg, start_insert=(width_px - width_px*0.12, height_px - height_px*0.88), num_cubes=12, size_increment=0, x_angle=0,
                         y_angle=0, z_angle=0, size=15, gap=5)

    panel_width = config["panel_width"]
    panel_height = config["panel_height"]
    panel_x = width_px - panel_width - config["panel_x_offset"]
    panel_y = config["panel_y_offset"]
    dwg.add(dwg.rect(insert=(panel_x, panel_y), size=(panel_width, panel_height),
                     fill=fill_color, stroke=fill_color, rx=5, ry=5))

    name_text = config["name"]
    padding = 10

    phone = config["phone"]
    email = config["email"]
    job_title = config["job_title"]
    org = config["org"]
    url = config["url"]

    y_offset = height_px - padding - 5
    for line in [
        "✉ " + email,
        "☎ " + phone,
        org,
        url]:
        dwg.add(dwg.text(line,
                         insert=(padding+5, y_offset),
                         font_size="8px", font_family="AvantGarde LT CondMedium", fill="white"
                         ))
        y_offset -= 10
    y_offset -= 10
    dwg.add(dwg.text(
        name_text,
        insert=(padding+5, y_offset),
        font_size="18px", font_family="AvantGarde LT CondMedium", fill="white"))
    y_offset -= 20

    dwg.add(dwg.text(job_title,
                     insert=(padding+5, y_offset),
                     font_size="14px", font_family="AvantGarde LT CondMedium", fill="white"
                     ))
    make_colored_qr_code(name=name_text, phone=phone, email=email, url=url, filename="qr_code.svg", back_color=back_color, fill_color=fill_color)
    qr_code_x, qr_code_y = config["qr_code_x"], config["qr_code_y"]
    qr_code_size = config["qr_code_size"]

    dwg.add(dwg.image(href="qr_code.svg", insert=(qr_code_x+10, qr_code_y+10), size=(qr_code_size, qr_code_size)))

    frame_size = 10
    stroke_color = "white"
    stroke_width = 2

    dwg.add(dwg.rect(insert=(qr_code_x + 10 -5, qr_code_y + 10-5), size=(frame_size, stroke_width), fill=stroke_color))
    dwg.add(dwg.rect(insert=(qr_code_x + 10 -5, qr_code_y + 10-5), size=(stroke_width, frame_size), fill=stroke_color))

    dwg.add(
        dwg.rect(insert=(qr_code_x + 10 + qr_code_size - frame_size + 5, qr_code_y + 5), size=(frame_size, stroke_width),
                 fill=stroke_color))
    dwg.add(
        dwg.rect(insert=(qr_code_x + 10 + qr_code_size - stroke_width + 5, qr_code_y + 5), size=(stroke_width, frame_size),
                 fill=stroke_color))

    dwg.add(
        dwg.rect(insert=(qr_code_x + 10 -5, qr_code_y + 10 + qr_code_size - stroke_width+5), size=(frame_size, stroke_width),
                 fill=stroke_color))
    dwg.add(
        dwg.rect(insert=(qr_code_x + 10 -5, qr_code_y + 10 + qr_code_size - frame_size +5), size=(stroke_width, frame_size),
                 fill=stroke_color))

    dwg.add(dwg.rect(insert=(qr_code_x + 10 + qr_code_size - frame_size +5, qr_code_y + 10 + qr_code_size - stroke_width +5),
                     size=(frame_size, stroke_width), fill=stroke_color))
    dwg.add(dwg.rect(insert=(qr_code_x + 10 + qr_code_size - stroke_width +5, qr_code_y + 10 + qr_code_size - frame_size +5),
                     size=(stroke_width, frame_size), fill=stroke_color))

    # dwg.add(dwg.text(f"{seed}",
    #                  insert=(width_px - 20, height_px - 1),
    #                  font_size="3px", font_family="AvantGarde LT CondMedium", fill="white", text_anchor="end"))

    dwg.save()

    business_card_back = svgwrite.Drawing("business_card_back.svg", size=(f"{width_px}px", f"{height_px}px"))
    business_card_back.add(business_card_back.rect(insert=(0, 0), size=(width_px, height_px),
                     fill=fill_color, stroke=fill_color, stroke_width=border_width))

    create_fading_grid(business_card_back, start_insert=(width_px - width_px*0.05, height_px - height_px*0.075), width=width_px*4 // 4+10, height=height_px // 3 - 5,
                       square_size=5, spacing=5, max_opacity=0.5)

    create_fading_grid(business_card_back, start_insert=(width_px - width_px * 0.05, height_px - height_px * 0.6),
                       width=width_px * 4 // 4 + 10, height=height_px // 2.5 - 5,
                       square_size=5, spacing=5, max_opacity=0.5)

    create_protein_chain(business_card_back, start_insert=(width_px - width_px*0.08, height_px - height_px*0.49), num_cubes=24, size_increment=0, x_angle=0,
                         y_angle=0, z_angle=50, size=16, gap=5)
    business_card_back.add(business_card_back.text(f"{version}",
                     insert=(panel_x + 5, panel_y),
                     font_size="8px", font_family="AvantGarde LT CondMedium", fill="white"))

    back_qr_code()


    business_card_back.add(business_card_back.image(href="qr_code_back.svg", insert=(10, 10), size=(30, 30)))

    business_card_back.add(
        business_card_back.rect(insert=(7, 7), size=(frame_size, stroke_width),
                 fill=stroke_color))
    business_card_back.add(
        business_card_back.rect(insert=(7, 7), size=(stroke_width, frame_size),
                 fill=stroke_color))

    business_card_back.add(
        business_card_back.rect(insert=(7, 41), size=(frame_size, stroke_width),
                 fill=stroke_color))
    business_card_back.add(
        business_card_back.rect(insert=(7, 33), size=(stroke_width, frame_size),
                 fill=stroke_color))

    business_card_back.add(
        business_card_back.rect(insert=(33, 7),
                     size=(frame_size, stroke_width), fill=stroke_color))
    business_card_back.add(
        business_card_back.rect(insert=(41, 7),
                     size=(stroke_width, frame_size), fill=stroke_color))

    business_card_back.add(
        business_card_back.rect(insert=(33, 41),
                     size=(frame_size, stroke_width), fill=stroke_color))
    business_card_back.add(
        business_card_back.rect(insert=(41, 33),
                     size=(stroke_width, frame_size), fill=stroke_color))


    business_card_back.add(business_card_back.text(f"{seed}",
                     insert=(width_px - 20, height_px - 2),
                     font_size="6px", font_family="AvantGarde LT CondMedium", fill="white", text_anchor="end"))

    business_card_back.save()

