"""
image_info.py
--------------
Helper functions related to the uploaded image.
Isse hum uploaded image ki basic details nikalte hain
(file name, size, format, dimensions, mode) taake
UI mein "Image Information" table dikha sakein.
"""

from PIL import Image


def get_image_information(uploaded_file):
    """
    Uploaded Streamlit file object se image ki information nikalta hai.

    Parameters
    ----------
    uploaded_file : streamlit UploadedFile
        User ne jo file upload ki hai.

    Returns
    -------
    dict
        Image ki properties (readable format mein).
    """

    # File pointer ko shuru se padhne ke liye reset karo
    uploaded_file.seek(0)

    image = Image.open(uploaded_file)

    width, height = image.size

    # File size ko bytes se readable format (KB / MB) mein convert karo
    file_size_bytes = len(uploaded_file.getvalue())
    file_size_kb = file_size_bytes / 1024

    if file_size_kb >= 1024:
        file_size_display = f"{file_size_kb / 1024:.2f} MB"
    else:
        file_size_display = f"{file_size_kb:.2f} KB"

    info = {
        "File Name": uploaded_file.name,
        "File Format": image.format if image.format else "Unknown",
        "File Size": file_size_display,
        "Dimensions (W x H)": f"{width} x {height} px",
        "Color Mode": image.mode,
    }

    # Pointer ko wapas shuru mein le jao taake baaki code bhi
    # isi file ko dobara padh sake
    uploaded_file.seek(0)

    return info
