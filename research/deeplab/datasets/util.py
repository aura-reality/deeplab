import os

def list_images(path):
    return [f for f in os.listdir(path) if not f.startswith('.')]

def parse_image_path(path):
    name, extension = os.path.basename(path).rsplit('.', 1)
    l = extension.lower()
    if l == "jpg" or l == "jpeg":
        return (name, "jpg")
    elif l == "png":
        return (name, "png")
    else:
        raise ValueError(l)
