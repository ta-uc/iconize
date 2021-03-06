from flask import (
    make_response, Blueprint, jsonify, current_app, send_file,abort
)
import io
import os
from iconize.utils.img import createImg
from iconize.utils.dbOpe import get_post
from iconize.db import Post, db
bp = Blueprint('staticFiles', __name__,)

import gzip

@bp.route('/posts/<iD>/content/', methods=['GET', 'POST'])
def give_content(iD):
    post = get_post(iD)
    if post is None:
        return ""
    res = make_response()
    # res.data = post.html
    res.data = gzip.compress(post.html)
    res.headers["Content-Encoding"] = "gzip"
    res.headers["Content-Type"] = "text/html"
    return res


@bp.route('/posts/<iD>/<int:size>.png')
def icon(size=512, iD=None):
    # pylint: disable=E1101
    if size > 512:
        return 'error'
    filename = 'icon.png'
    res = make_response()
    # When uploaded file exists
    if db.session.query(Post.icon).filter(Post.iD == iD).scalar() is not None:
        post = get_post(iD)
        res.data = post.icon
    # When uploaded file does not exist
    else:
        post = get_post(iD)
        if post.color == '' or post.color is None:
            color = "#FFF"
        else:
            color = "#"+post.color
        text = post.s_title
        res.data = createImg(text, size=size, color=color)
    res.headers["Content-Disposition"] = 'filename=' + filename
    res.headers["Content-Type"] = "image/png"
    return res


@bp.route('/posts/<iD>/service-worker.js')
def sw(iD):
    post = get_post(iD)
    res = make_response()
    path = current_app.root_path + "/static/service-worker.js"
    with open(path) as f:
        rawSw = f.read()
    swjs = rawSw.replace("VERSION","'"+iD+"-"+str(post.ver)+"'")
    res.data = swjs
    fileName = "service-worker.js"
    res.headers['Content-Disposition'] = 'filename=' + fileName
    res.headers["Content-Type"] = "application/javascript"
    return res

@bp.route('/posts/<iD>/<path:path>')
@bp.route('/ce/<path:path>')
@bp.route('/base/<path:path>')
def return_staticfiles(iD=None,path="/"):
    path = current_app.root_path + "/" + path
    if ".js" in path:
        type = "application/javascript"
    elif ".css" in path:
        type = "text/css"
    else:
        return send_file(path)
    try:
        with open(path,"rb") as f:
            data = f.read()
            data_compressed = gzip.compress(data)
            res = make_response()
            res.data = data_compressed
            res.headers["Content-Encoding"] = "gzip"
            res.headers["Content-Type"] = type
            return res
    except:
        return abort(404)

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
    bg_color = "#F2F2F2" if color in ("FFF","FFFFFF",) else "#FFF"
    json_data = {
        "name": title,
        "short_name": s_title,
        "theme_color": "#"+color,
        "background_color": bg_color,
        "display": "fullscreen",
        "orientation": "portrait",
        "scope": "/posts/"+iD+"/",
        "start_url": "/posts/" + iD + "/",
        "icons": [
            {"src": '/posts/'+iD+'/512.png',
             "sizes": "512x512",
             "type": "image/png"
             },
            {"src": '/posts/'+iD+'/256.png',
             "sizes": "256x256",
             "type": "image/png"
             },
            {"src": '/posts/'+iD+'/128.png',
             "sizes": "128x128",
             "type": "image/png"
             }]
    }
    return jsonify(json_data)
