from flask import (
    make_response, Blueprint, url_for, jsonify,current_app,send_file
)
import io
import os
from ..utils.img import createImg
from ..utils.dbOpe import get_post
from ..db import Post, db
bp = Blueprint('staticFiles', __name__,)


@bp.route('/<iD>/content/', methods=['GET', 'POST'])
def give_content(iD):
    post = get_post(iD)
    if post is None:
        return ""
    res = make_response()
    res.data = post.html
    res.headers["Content-Type"] = "text/html"
    return res


@bp.route('/<iD>/<int:size>.png')
def icon(size=512, iD=None):
    # pylint: disable=E1101
    if size > 512:
        return 'error'
    filename = 'icon.png'
    res = make_response()
    if db.session.query(Post.icon).filter(Post.iD == iD).scalar() is not None:
        post = get_post(iD)
        res.data = post.icon
    else:
        post = get_post(iD)
        if post.color == '' or post.color is None:
            color = "#FFF"
        else:
            color = "#"+post.color
        text = post.s_title
        iconstorage = io.BytesIO()
        imgobj = createImg(text, size=size, color=color)
        imgobj.save(iconstorage, 'png')
        iconfile = iconstorage.getvalue()
        res.data = iconfile
        iconstorage.close()
    res.headers["Content-Disposition"] = 'filename=' + filename
    res.headers["Content-Type"] = "image/png"
    return res


@bp.route('/service-worker.js')
def sw():
    res = make_response()
    path = current_app.root_path + "/static/service-worker.js"
    with open(path) as sw:
        res.data = sw.read()
    fileName = "service-worker.js"
    res.headers['Content-Disposition'] = 'filename=' + fileName
    res.headers["Content-Type"] = "application/javascript"
    return res


# @bp.route("/favicon.ico")
# def favicon():
#     res = make_response()
#     path = current_app.root_path + "/static/favicon.ico"
#     with open(path) as ico:
#         res.data = ico
#     fileName = "favicon.ico"
#     res.headers['Content-Disposition'] = 'filename=' + fileName
#     res.headers["Content-Type"] = "image/x-icon"
#     return res

@bp.route("/favicon.ico")
def favicon():
    path = current_app.root_path + "/static/favicon.ico"
    return send_file(path)


@bp.route('/posts/<iD>/manifest.json')
def manifest(iD=None):
    post = get_post(iD)
    title = post.title
    s_title = post.s_title
    color = post.color or "FFF"
    json_data = {
        "name": title,
        "short_name": s_title,
        "theme_color": "#"+color,
        "background_color": "#FFF",
        "display": "standalone",
        "orientation": "portrait",
        "scope": "/posts/",
        "start_url": "/posts/" + iD + "/",
        "icons": [
            {"src": '/'+iD+'/512.png',
             "sizes": "512x512",
             "type": "image/png"
             },
            {"src": '/'+iD+'/256.png',
             "sizes": "256x256",
             "type": "image/png"
             },
            {"src": '/'+iD+'/128.png',
             "sizes": "128x128",
             "type": "image/png"
             }]
    }
    return jsonify(json_data)
