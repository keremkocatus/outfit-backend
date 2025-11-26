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
        return "Extract the bag, belt, hat, glasses, jewelry from the image. Preserve the clothing exactly as it is. Remove background and body parts."

    else:
        return "Extract the clothing item from the image without changing its shape or size. Preserve the clothing exactly as it is. Remove background and human body parts."


def get_tryon_input(category: str) -> str:
    return f"""
        Generate a photorealistic virtual try-on result.

        The first input image is the **model image**, which must remain exactly the same person:
        - Keep the model's identity, face, pose, body shape, skin tone, and background unchanged.

        The second input image is the **garment image**, containing the clothing item(s) that must be applied onto the model.

        Garment Transfer Rules:
        - Garment category: {category}
        - If 'tops': replace ONLY the upper-body clothing.
        - If 'bottoms': replace ONLY the pants/skirts/shorts.
        - If 'one-pieces': replace the full-body garment appropriately.
        - Preserve all garment attributes: texture, colors, patterns, logos, stitching, fabric behavior, and shape.
        - Ensure realistic physics: natural draping, correct alignment, shadows, wrinkles, and body interaction.
        - The output must look like a real photograph with consistent lighting and perspective.
        - Do NOT change the model’s appearance except for the clothing replacement.

        Output:
        A highly realistic image of the model wearing the garment(s) exactly as shown in the garment image.
        """