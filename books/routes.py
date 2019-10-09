from flask import Blueprint, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash

from application import db
from books.models import Review

book_app = Blueprint('book_app', __name__)

