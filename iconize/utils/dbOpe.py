from ..db import db, Post, init_db
from flask import current_app as app, g
import datetime
def get_post(iD=None):
    return Post.query.filter(Post.iD == iD).first()


def get_post_list(num=0):
    try:
        list_of_posts = Post.query.order_by(
            Post.created_date.desc()).limit(num)
    except:
        init_db(app)
        list_of_posts = Post.query.order_by(
            Post.created_date.desc()).limit(num)
    return list_of_posts


def delete_post(iD=None):
    # pylint: disable=E1101
    post = db.session.query(Post).filter(Post.iD == iD).first()
    db.session.delete(post)
    db.session.commit()


def add_post(iD=None, author=None, html=None, title=None,
             s_title=None, color=None, date=None, token=None):
    # pylint: disable=E1101
    post = Post()
    post.iD = iD
    post.author = author
    post.html = html.encode()
    post.title = title
    post.s_title = s_title
    post.color = color
    post.date = date
    post.token = token
    db.session.add(post)
    db.session.commit()


def mod_post(iD, author=None, html=None, title=None,
             s_title=None, color=None, date=None, icon=None):
    # pylint: disable=E1101
    post = db.session.query(Post).filter(Post.iD == iD).first()
    post.author = author if author is not None else post.author
    post.html = html.encode() if html is not None else post.html
    post.title = title if title is not None else post.title
    post.s_title = s_title if s_title is not None else post.s_title
    post.color = color if color is not None else post.color
    post.date = date if date is not None else post.date
    post.icon = icon if icon is not None else post.icon
    post.ver += 1
    post.updated_date = datetime.date.today()
    db.session.add(post)
    db.session.commit()
