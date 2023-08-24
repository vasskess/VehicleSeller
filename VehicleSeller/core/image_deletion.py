from cloudinary import api


def delete_image(instance):
    cloudinary_file = instance
    cloudinary_public_id = cloudinary_file.public_id

    api.delete_resources(public_ids=[cloudinary_public_id])
