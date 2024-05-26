import os
from PIL import Image

default_shade = 128

os.system("title PracticalOCR")

default_color_choice = "01"
color_id = {"white": "1", "light": "1", "w": "1", "black": "0", "dark": "0", "b": "0"}
default_size = (100, 1)

folder = "shapes"
chars = {"a": {"min": (3, 3), "pass": 0.7},
         "b": {"min": (3, 3), "pass": 0.7},
         "c": {"min": (3, 3), "pass": 0.7},
         "d": {"min": (3, 3), "pass": 0.7},
         "e": {"min": (3, 3), "pass": 0.7},
         "f": {"min": (3, 3), "pass": 0.7},
         "g": {"min": (3, 3), "pass": 0.7},
         "h": {"min": (3, 3), "pass": 0.7},
         "i": {"min": (1, 2), "simple": True, "pass": 0.7},
         "j": {"min": (3, 3), "pass": 0.7},
         "k": {"min": (3, 3), "pass": 0.7},
         "l": {"min": (1, 3), "simple": True, "pass": 0.7},
         "m": {"min": (3, 3), "pass": 0.7},
         "n": {"min": (3, 3), "pass": 0.7},
         "o": {"min": (3, 3), "pass": 0.7},
         "p": {"min": (3, 3), "pass": 0.7},
         "q": {"min": (3, 3), "pass": 0.7},
         "r": {"min": (1, 2), "pass": 0.7},
         "s": {"min": (3, 3), "pass": 0.7},
         "t": {"min": (3, 3), "pass": 0.7},
         "u": {"min": (3, 3), "pass": 0.7},
         "v": {"min": (3, 3), "pass": 0.7},
         "w": {"min": (3, 3), "pass": 0.7},
         "x": {"min": (3, 3), "pass": 0.7},
         "y": {"min": (3, 3), "pass": 0.7},
         "z": {"min": (1, 2), "pass": 0.7},
         "A": {"min": (3, 3), "pass": 0.7},
         "B": {"min": (3, 3), "pass": 0.7},
         "C": {"min": (3, 3), "pass": 0.7},
         "D": {"min": (3, 3), "pass": 0.7},
         "E": {"min": (3, 3), "pass": 0.7},
         "F": {"min": (3, 3), "pass": 0.7},
         "G": {"min": (3, 3), "pass": 0.7},
         "H": {"min": (3, 3), "pass": 0.7},
         "I": {"min": (1, 2), "pass": 0.7},
         "J": {"min": (3, 3), "pass": 0.7},
         "K": {"min": (3, 3), "pass": 0.7},
         "L": {"min": (3, 3), "pass": 0.7},
         "M": {"min": (3, 3), "pass": 0.7},
         "N": {"min": (3, 3), "pass": 0.7},
         "O": {"min": (3, 3), "simple": True, "pass": 0.7},
         "P": {"min": (3, 3), "pass": 0.7},
         "Q": {"min": (3, 3), "pass": 0.7},
         "R": {"min": (1, 2), "pass": 0.7},
         "S": {"min": (3, 3), "pass": 0.7},
         "T": {"min": (3, 3), "pass": 0.7},
         "U": {"min": (3, 3), "pass": 0.7},
         "V": {"min": (3, 3), "pass": 0.7},
         "W": {"min": (3, 3), "pass": 0.7},
         "X": {"min": (3, 3), "pass": 0.7},
         "Y": {"min": (3, 3), "pass": 0.7},
         "Z": {"min": (1, 2), "pass": 0.7},
         "0": {"min": (3, 3), "pass": 0.7},
         "1": {"min": (1, 2), "pass": 0.7},
         "2": {"min": (3, 3), "pass": 0.7},
         "3": {"min": (3, 3), "pass": 0.7},
         "4": {"min": (3, 3), "pass": 0.7},
         "5": {"min": (3, 3), "pass": 0.7},
         "6": {"min": (3, 3), "pass": 0.7},
         "7": {"min": (3, 3), "pass": 0.7},
         "8": {"min": (3, 3), "pass": 0.7},
         "9": {"min": (1, 2), "pass": 0.7},
         "i.": {"min": (1, 1), "simple": True, "pass": 0.5}}
support = ["", "i."]

def image_list(image, shade=default_shade):
    width, height = image.size
    pixel_values = [[0 for x in range(width)] for y in range(height)]
    chunk_div = int(width / 20)
    if chunk_div < 5:
        chunk_div = 5
    for x in range(width):
        for y in range(height):
            value = 0
            for i in image.getpixel((x, y))[0:3]:
                value += i
            pixel_values[y][x] = int(value / 3)
            pixel_values[y][x] = (lambda x: {False: "0", True: "1"}[x > shade])(pixel_values[y][x])
    return pixel_values

def get_object_list(pixel_values, color=default_color_choice):
    if color in color_id:
        color = color_id[color]
    width, height = len(pixel_values[-1]), len(pixel_values)
    object_list = {}
    current_object = 0
    links = {}
    def create_object_id(y, x):
        nonlocal current_object, links, object_list
        current_object += 1
        links[current_object] = current_object
        object_list[current_object] = {"type": "", "chance": 0, "y": [y, y], "x": [x, x], "color": {"0": "black", "1": "white"}[pixel_values[y][x]], "size": default_size}
        id_board[y][x] = current_object
    def link(item1, item2):
        merging_link = links[item1]
        new_link = links[item2]
        if merging_link == new_link:
            return
        for i in "yx":
            if object_list[merging_link][i][0] < object_list[new_link][i][0]:
                object_list[new_link][i][0] = object_list[merging_link][i][0]
        for i in "yx":
            if object_list[merging_link][i][1] > object_list[new_link][i][1]:
                object_list[new_link][i][1] = object_list[merging_link][i][1]
        links[merging_link] = links[new_link]
        for link in links:
            if links[link] == merging_link:
                links[link] = links[new_link]
        object_list.pop(merging_link)
    for z in color:
        id_board = [[0 for x in range(width)] for y in range(height)]
        for x in range(width):
            for y in range(height):
                if pixel_values[y][x] == z:
                    if y > 0:
                        if id_board[y - 1][x] != 0:
                            id_board[y][x] = id_board[y - 1][x]
                        else:
                            create_object_id(y, x)
                    else:
                        create_object_id(y, x)
                    if id_board[y][x] != 0:
                        if y > object_list[links[current_object]]["y"][1]:
                            object_list[links[current_object]]["y"][1] = y
                    if x > 0:
                        if y > 0:
                            if id_board[y - 1][x - 1] != 0:
                                link(id_board[y][x], id_board[y - 1][x - 1])
                        if id_board[y][x - 1] != 0:
                            link(id_board[y][x], id_board[y][x - 1])
                        if y + 1 < height:
                            if id_board[y + 1][x - 1] != 0:
                                link(id_board[y][x], id_board[y + 1][x - 1])
    return object_list

def get_object(obj, pixel_values):
    snip_board = []
    for y in range(obj["y"][0], obj["y"][1] + 1):
        snip_board += [pixel_values[y][obj["x"][0]: obj["x"][1] + 1]]
    return snip_board

# reading - image that will be read. color - what colors are to be read. singles - If single character lines are allowed.
def read_img(reading, color=default_color_choice, singles=True, min_size=(1, 1), min_font_size=0, max_font_size=1000000, fonts=range(10), return_mode="default", font_consistency=True, shade=default_shade, passing=0.95,
             space_occurance=2, new_line="\n"):
    if color in color_id:
        color = color_id[color]
    image = Image.open(reading)
    width, height = image.size
    pixel_values = image_list(image, shade=shade)
    object_list = get_object_list(pixel_values, color=color)
    pop_list = []
    reverse = {"0": "1", "1": "0"}
    sizes = []
    for obj in object_list:
        average_height = (0, 1000000)
        if len(sizes) >= 3:
            average_height = 0
            for i in sizes:
                average_height += i
            average_height /= len(sizes)
            average_height = (average_height / 1.2, average_height * 1.2)
        obj = object_list[obj]
        snip_board = get_object(obj, pixel_values)
        snip_y, snip_x = len(snip_board), len(snip_board[-1])
        for char in chars:
            char_name = char
            char = chars[char]
            matching = 0
            if char["min"][0] > snip_x or char["min"][1] > snip_y or min_size[0] > snip_x or min_size[1] > snip_y:
                continue
            for i in fonts:
                beginner = ""
                if char_name.isupper():
                    beginner = "C"
                img_loc = f"{folder}/{beginner}{char_name}_{i}.png"
                if not os.path.exists(img_loc):
                    break
                char["img"] = Image.open(img_loc)
                width_growth = snip_x / char["img"].size[0]
                height_growth = snip_y / char["img"].size[1]
                if min_font_size > height_growth or max_font_size < height_growth:
                    continue
                if font_consistency:
                    if height_growth < average_height[0] or height_growth > average_height[1]:
                        continue
                change = width_growth / height_growth
                if change >= 2 or change <= 0.5:
                    continue
                char_img = char["img"].resize((snip_x, snip_y), resample=Image.NEAREST)
                char_board = [[0 for x in range(snip_x)] for y in range(snip_y)]
                starter = color_id[obj["color"]]
                for x in range(snip_x):
                    for y in range(snip_y):
                        if char_img.getpixel((x, y))[0] > 127:
                            char_board[y][x] = reverse[starter]
                        else:
                            char_board[y][x] = starter
                matching = 0
                max_match = snip_y * snip_x
                for x in range(snip_x):
                    for y in range(snip_y):
                        if snip_board[y][x] == char_board[y][x]:
                            matching += 1
                matching = matching / max_match
                if False:
                    if char_name == "e" or char_name == "o":
                        input((char_name, matching, (width_growth, height_growth)))
                if matching < char["pass"]:
                    continue
                bonus = 0.05
                if width_growth == obj["size"][0]:
                    less_different = abs(1 - height_growth) <= abs(1 - obj["size"][1]) + (matching - obj["chance"])
                else:
                    less_different = abs(1 - width_growth / height_growth) <= abs(1 - obj["size"][0] / obj["size"][1]) + (matching - obj["chance"])
                if (matching > obj["chance"] + bonus and less_different
                    or matching > obj["chance"] and obj["type"] == "" and "simple" in char):
                    obj["type"] = char_name
                    obj["chance"] = matching
                    obj["size"] = (width_growth, height_growth)
            if matching > passing and "simple" not in char:
                break
        if font_consistency and obj["size"] != default_size:
            sizes += [obj["size"][1]]
    for i in pop_list:
        object_list.pop(i)
    string_list = {}
    current_row = 0
    def add_string_line(obj):
        nonlocal current_row, string_list
        if not singles:
            if current_row > 0:
                current_row_string = string_list[current_row]["s"]
                if len(current_row_string) == 1 or current_row_string.count(" ") >= len(current_row_string.replace(" ")):
                    string_list.pop(current_row)
        current_row += 1
        string_list[current_row] = {"s": obj["type"], "a": obj["y"], "x": obj["x"], "f": obj["size"]}
    pop_list = []
    for obj in object_list:
        obj = object_list[obj]
        if obj["type"] in support:
            continue
        for row_id in string_list:
            row = string_list[row_id]
            y_min, y_max = obj["y"]
            a_min, a_max = row["a"]
            if any(item in range(y_min, y_max + 1) for item in range(a_min, a_max + 1)):
                obj_height = obj["y"][1] - obj["y"][0] + 1
                distance = obj["x"][0] - row["x"][1]
                if distance > (obj_height / space_occurance):
                    string_list[row_id]["s"] += " "
                string_list[row_id]["s"] += obj["type"]
                string_list[row_id]["x"] = obj["x"]
                string_list[row_id]["f"] = obj["size"]
                break
        else:
            add_string_line(obj)
    string_list = [value["s"] for key, value in sorted(string_list.items(), key=lambda x: x[1]["a"][0])]
    full_text = ""
    for line in string_list:
        full_text += f"{line}{new_line}"
    if full_text:
        full_text = full_text[0:-1]
    match return_mode: # noqa
        case "default":
            return full_text
        case "list":
            return string_list
        case "object":
            return object_list
        case "pixels":
            return pixel_value
