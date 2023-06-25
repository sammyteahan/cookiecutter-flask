from flask import Blueprint
from flask import render_template

page = Blueprint("page", __name__, template_folder="templates")


@page.get("/")
def home():
    return render_template("page/home.html")
