from PIL import Image
import os
import practicalOCR

if not os.path.exists("font_0.png"):
    os.system("mode 25, 3")
    input("font_0.png not found.")
    exit()
if os.path.exists("fonts.py"):
    import fonts
font_details = []
for font in range(10):
    if font in fonts.data:
        font_details += [fonts.data[font]]
    else:
        font_details += [{}]

char_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
             "CA", "CB", "CC", "CD", "CE", "CF", "CG", "CH", "CI", "CJ", "CK", "CL", "CM", "CN", "CO", "CP", "CQ", "CR", "CS", "CT", "CU", "CV", "CW", "CX", "CY", "CZ",
             "a", "b", "c", "d", "e", "f", "g", "h", "i.", "i", "i.", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",]
for i in fonts.read:
    if not os.path.exists(f"font_{i}.png"):
        break
    image = Image.open(f"font_{i}.png")
    shade = 128
    char_list_replica = char_list.copy()
    font_data = fonts.data_override.copy()
    if i in fonts.data:
        font_data.update(fonts.data[i].copy())
    if "shade" in font_data:
        shade = font_data["shade"]
    if "no_lowercase" in font_data:
        if font_data["no_lowercase"]:
            char_list_replica = char_list_replica[0:-28]
    if "no_capital" in font_data:
        if font_data["no_capital"]:
            char_list_replica = char_list_replica[0:10] + char_list_replica[36::]
    if "no_number" in font_data:
        if font_data["no_number"]:
            char_list_replica = char_list_replica[10::]
    pixel_values = practicalOCR.image_list(image, shade=shade)
    object_list = practicalOCR.get_object_list(pixel_values, color="b")
    if len(object_list) > len(char_list_replica):
        os.system("mode 75, 5")
        print(f"font_{i}.png contains too much or too little characters.")
        print("It may have been read incorrectly. Letters may have been too thin.")
        input("You can try to tweak the shade setting on your font in fonts.py.")
        exit()
    elif len(object_list) < len(char_list_replica):
        os.system("mode 75, 6")
        print(f"font_{i}.png contains too much or too little characters.")
        print("Is something excluded? Read up on Manual.txt * TWEAKING THE FONT")
        print("It may have been read incorrectly. Letters may have been too thick.")
        input("You can try to tweak the shade setting on your font in fonts.py.")
        exit()
    overlapping_objects = {}
    current_row = 0
    for obj_id in object_list:
        obj = object_list[obj_id]
        x_min, x_max = obj["x"]
        obj_width, obj_height = (x_max - x_min + 1), obj["y"][1] - obj["y"][0] + 1
        if obj_width / obj_height > fonts.width_limit:
            os.system("mode 75, 7")
            print(f"Abnormally wide character spotted in font_{i}.png.")
            print(f"Make sure that the formatting of font_{i}.png is correct.")
            print("Try decreasing the shade setting on your font in fonts.py.")
            print("Alternatively, increase the size between the characters.")
            input("Or increase the width_limit in fonts.py.")
        for row_id in overlapping_objects:
            row = overlapping_objects[row_id]
            a_min, a_max = row["a"]
            if sum(item in range(x_min, x_max + 1) for item in range(a_min, a_max + 1)) >= obj_width / 5:
                overlapping_objects[row_id]["s"] += [obj_id]
                overlapping_objects[row_id]["y"] += [obj["y"][0]]
                if x_min > row["a"][0]:
                    overlapping_objects[row_id]["a"][1] = x_min
                if x_max > row["a"][1]:
                    overlapping_objects[row_id]["a"][1] = x_max
                break
        else:
            current_row += 1
            overlapping_objects[current_row] = {"s": [obj_id], "a": obj["x"], "y": [obj["y"][0]]}
    for obj_id in overlapping_objects.copy():
        row = overlapping_objects[obj_id]
        if len(row["s"]) == 1:
            overlapping_objects.pop(obj_id)
        elif len(row["s"]) > 2:
            os.system("mode 75, 5")
            print(f"A character was found in font_{i}.png that is split into 3.")
            print(f"Make sure that the formatting of font_{i}.png is correct.")
            input("Try increasing the shade setting on your font in fonts.py.")
            exit()
        else:
            allowed_pool = [char_list.index("i."), char_list.index("i"), char_list.index("j") - 1, char_list.index("j")]
            row["s"] = [list(object_list.keys()).index(row["s"][0]), list(object_list.keys()).index(row["s"][1])]
            if row["s"][0] not in allowed_pool or row["s"][1] not in allowed_pool:
                os.system("mode 75, 4")
                input(f"{row['s']} in {allowed_pool}")
                print(f"An unidentified character was found in font_{i}.png.")
                input("Try increasing the shade setting on your font in fonts.py.")
                exit()
            if row["y"][0] > row["y"][1]:
                row["s"].sort()
                if row["s"] == allowed_pool[0:2]:
                    char_list_replica[char_list.index("i.")] = "i"
                    char_list_replica[char_list.index("i")] = "i."
                if row["s"] == allowed_pool[2:4]:
                    char_list_replica[char_list.index("j") - 1] = "j"
                    char_list_replica[char_list.index("j")] = "i."
    if not len(overlapping_objects):
        while "i." in char_list_replica:
            char_list_replica.remove("i.")
    board_list = []
    for obj in object_list:
        board_list += [practicalOCR.get_object(object_list[obj], pixel_values)]
    for board in range(len(board_list)):
        for row in range(len(board_list[board])):
            for column in range(len(board_list[board][row])):
                board_list[board][row][column] = {"0": (0, 0, 0), "1": (255, 255, 255)}[board_list[board][row][column]]
    index = -1
    for board in board_list:
        index += 1
        width, height = len(board[-1]), len(board)
        image = Image.new('RGB', (width, height))
        for y, row in enumerate(board):
            for x, color in enumerate(row):
                image.putpixel((x, y), color)
        image.save(f"shapes/{char_list_replica[index]}_{i}.png")
os.system("mode 30, 3")
input("Training was successful.")
