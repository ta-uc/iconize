import os
import io
from .img import make512
from .dbOpe import get_post,mod_post
from ..db import Post,db

def saveFile(icon=None,name=None):
    if icon.filename.rsplit('.', 1)[1].lower() == 'png':
        iconfile = icon
    else:
        return "error"
    if iconfile:
        iconpng = make512(iconfile)
        output = io.BytesIO()
        iconpng.save(output, format='PNG')
        icon = output.getvalue()
        mod_post(iD=name,icon=icon)

def deleteFile(iD=None):
    if iD is not None:
        # pylint: disable=E1101
        post = get_post(iD)
        post.icon = None
        db.session.add(post)
        db.session.commit()