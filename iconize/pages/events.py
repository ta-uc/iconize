from flask import (
    make_response, Blueprint, flash, g, redirect,
    render_template, request, url_for, jsonify
)
from ..db import Post
from ..utils.dbOpe import get_post, delete_post, get_post_list, add_post, mod_post
from ..utils.cleaner import cl
from ..utils.dataHash import getHash
from ..utils.img import make512
from ..utils.fileOpe import saveFile, deleteFile
import os

bp = Blueprint('events', __name__, url_prefix='/posts/')


@bp.route('/', methods=['GET'])
def list_posts():
    num = 10
    list_of_posts = get_post_list(num)
    num_of_posts = list_of_posts.count()
    return render_template('/events/index.html', posts=list_of_posts, num=num_of_posts)


@bp.route('/create/', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':

        title = request.form["title"]
        s_title = request.form["s_title"]
        if s_title == "":
            s_title = title
        data = request.files["code"]
        html = data.read()
        html = html.decode("utf-8")
        cleaned_html = cl(html)
        returnValue = getHash(html)
        iD = returnValue[0]
        token = returnValue[1]
        add_post(iD, request.form['author'], cleaned_html,
                 request.form['title'], s_title,
                 request.form['color'], request.form['date'], token)
        if "iconfile" in request.files:
            saveFile(icon=request.files["iconfile"], name=iD)
        return jsonify(returnValue)

    access_type = "Create"
    return render_template('/events/content.html', access_type=access_type)


@bp.route('/<iD>/edit/', methods=['GET', 'POST'])
def edit_post(iD):
    token_data = get_post(iD)
    if token_data is None:
        return redirect('/')
    token = token_data.token

    if request.method == 'POST':
        try:
            title = request.form["title"]
            s_title = request.form['s_title']
            if s_title == '':
                s_title = title
            if request.form["del"]:
                deleteFile(iD)
            if "iconfile" in request.files:
                saveFile(icon=request.files["iconfile"], name=iD)
            data = request.files["code"]
            html = data.read()
            html = html.decode("utf-8")
            cleaned_html = cl(html)
            mod_post(iD, request.form['author'], cleaned_html,
                     request.form['title'], s_title,
                     request.form['color'], request.form['date'])
        except:
            return 'error'
        return 'success'

    if request.method == 'GET':
        if request.args.get('token') == '' or request.args.get('token') is None:
            return render_template('events/content.html', auth='missing', html='')
        if request.args.get('token') != token:
            return render_template('events/content.html', auth='incorrect', html='')
        post = get_post(iD)
        access_type = "Edit"
        return render_template('events/content.html', access_type=access_type,
                               author=post['author'], auth='success', title=post['title'],
                               s_title=post['s_title'], date=post['date'], color=post['color'])


@bp.route('/<iD>/', methods=['GET'])
def show_post(iD=None):
    post = get_post(iD)
    if post is None:
        return "This page doesn't exist or the page iD is incorrect."
    return render_template('/events/show_post.html', title=post.title, iD=iD,
                           date=post.date, author=post.author, s_title=post.s_title, color=post.color)


@bp.route('/<iD>/delete/', methods=['GET', 'POST'])
def delete(iD):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        token_data = get_post(iD)

        if token_data == "" or token_data is None:
            return "error"

        token = token_data.token

        if request.form["token"] == "" or request.form["token"] is None or token != request.form["token"]:
            return "error"

        delete_post(iD)
        return "Success"
