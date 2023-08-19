from cloudinary import api


# TODO This may needs to be moved, since it will serve not only vehicle_image deletion !
def delete_image(instance):
    cloudinary_file = instance.vehicle_image
    cloudinary_public_id = cloudinary_file.public_id

    api.delete_resources(public_ids=[cloudinary_public_id])
