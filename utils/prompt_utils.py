def get_enhance_prompt(category: str) -> str:
    if category == "tops":
        return "Extract only the top clothing item (t-shirt, polo t-shirt,shirt, blouse) from the image. Preserve the clothing exactly as it is. Remove background and all human body parts."

    elif category == "longtops":
        return "Extract the dress from the image. Preserve the clothing exactly as it is. Keep full original length and remove background and human parts."

    elif category == "bottoms":
        return "Extract only the bottom clothing item (pants, shorts, skirt) from the image. Preserve the clothing exactly as it is. Keep its exact length, remove background and body parts."

    elif category == "one-pieces":
        return "Extract all clothing items from the person together as they appear. Preserve the clothing exactly as it is. Remove background and human body parts."

    elif category == "shoes":
        return "Extract the pair of shoes from the image in their original shape and view. Preserve the clothing exactly as it is. Remove background and body parts."

    elif category == "accessories":
        return "Extract the accessory (bag, belt, hat, glasses, jewelry) from the image. Preserve the clothing exactly as it is. Remove background and body parts."

    else:
        return "Extract the clothing item from the image without changing its shape or size. Preserve the clothing exactly as it is. Remove background and human body parts."
