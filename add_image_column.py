IMAGE_URL = "https://res.cloudinary.com/dgira6yxf/image/upload/v1765614396/dvdqkqprn0quoo0tppii.png,dvdqkqprn0quoo0tppii"

input_file = "students.csv"
output_file = "students_with_images.csv"

with open(input_file, "r", encoding="utf-8") as infile, \
     open(output_file, "w", encoding="utf-8") as outfile:

    for line in infile:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        new_line = [parts[0], IMAGE_URL] + parts[1:]
        outfile.write(",".join(new_line) + "\n")

print("✅ Image URL added to all records.")