from src import models, db
from src.libs.file_service import move_user_picture


def get_pictures_user(user_id):
    return db.session.query(models.Picture).filter(models.Picture.user_id == user_id).all()


def upload_file_for_user(user_id, file_path, description):
    new_filename, size = move_user_picture(user_id, file_path)
    picture = models.Picture(description=description, user_id=user_id, path=new_filename, size=size)
    db.session.add(picture)
    db.session.commit()