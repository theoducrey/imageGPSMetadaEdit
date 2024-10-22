import os
import shutil
import pyheif
from PIL import Image
import exifread
import re


def convert_heic_to_jpg(heic_path, jpg_path):
    """Convert HEIC image to JPG format."""
    heif_file = pyheif.read(heic_path)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride
    )
    image.save(jpg_path, "JPEG")


def convert_png_to_jpg(png_path, jpg_path):
    """Convert PNG image to JPG format."""
    image = Image.open(png_path)
    # Convert image to RGB to remove alpha channel if present
    rgb_image = image.convert('RGB')
    rgb_image.save(jpg_path, "JPEG")


def get_image_taken_year(image_path):
    """Extract the year the image was taken from its metadata."""
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, stop_tag="EXIF DateTimeOriginal")
        date_taken = tags.get("EXIF DateTimeOriginal")
        if date_taken:
            return date_taken.values[:4]
    return None


def main(folder_path):
    # Extract the year from the folder name using regex
    folder_name = os.path.basename(folder_path)
    folder_year_match = re.search(r'\b(\d{4})\b', folder_name)
    folder_year = folder_year_match.group(1) if folder_year_match else None

    if not folder_year:
        print("No valid year found in the folder name.")
        return

    # Process each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Convert HEIC to JPG if needed
        if file_name.lower().endswith('.heic'):
            jpg_path = os.path.splitext(file_path)[0] + '.jpg'
            print(f"Converting {file_name} to {os.path.basename(jpg_path)}...")
            convert_heic_to_jpg(file_path, jpg_path)

        # Convert PNG to JPG if needed
        if file_name.lower().endswith('.png'):
            jpg_path = os.path.splitext(file_path)[0] + '.jpg'
            print(f"Converting {file_name} to {os.path.basename(jpg_path)}...")
            convert_png_to_jpg(file_path, jpg_path)

        # Check for associated MOV file
        base_name, ext = os.path.splitext(file_name)
        mov_file_path = os.path.join(folder_path, base_name + '.mov')
        if os.path.exists(mov_file_path):
            # Show the image to the user
            if ext.lower() in ['.jpg', '.jpeg', '.png']:
                with Image.open(file_path) as img:
                    img.show()

            # Prompt the user to keep or remove the MOV file
            action = input(f"Keep MOV file '{base_name}.mov'? Type 'g' to keep or 'p' to remove: ").strip().lower()
            if action == 'p':
                os.remove(mov_file_path)
                print(f"Removed {base_name}.mov")
            else:
                print(f"Kept {base_name}.mov")

        # Verify the year the picture was taken
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            image_taken_year = get_image_taken_year(file_path)
            if image_taken_year and image_taken_year != folder_year:
                print(f"Warning: {file_name} was taken in {image_taken_year}, but the folder indicates {folder_year}.")


if __name__ == "__main__":
    folder_path = input("Enter the path to the folder: ").strip()
    main(folder_path)
