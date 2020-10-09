from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Paper %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/news')
def news():
    papers = Paper.query.order_by(Paper.date.desc()).all()
    return render_template("news.html", papers = papers)


@app.route('/news/<int:id>')
def news_detail(id):
    paper = Paper.query.get(id)
    return render_template("news_detail.html", paper = paper)


@app.route('/news/<int:id>/delete')
def news_delete(id):
    paper = Paper.query.get_or_404(id)

    try:
        db.session.delete(paper)
        db.session.commit()
        return redirect('/news')
    except:
        return "При удалении статьи произошла ошибка!!!"


@app.route('/news/<int:id>/update', methods=['POST', 'GET'])
def news_update(id):
    paper = Paper.query.get(id)
    if request.method == "POST":
        paper.title = request.form['title']
        paper.intro = request.form['intro']
        paper.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/news')
        except:
            return "При редактировании статьи произошла ошибка!!!"
    else:
        return render_template("news_update.html", paper=paper)


@app.route('/create-paper', methods=['POST', 'GET'])
def create_paper():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        paper = Paper(title = title, intro = intro, text = text)

        try:
            db.session.add(paper)
            db.session.commit()
            return redirect('/news')
        except:
            return "При добавлении статьи произошла ошибка!!!"
    else:
        return render_template("create-paper.html")


if __name__ == '__main__':
    app.run(debug = True)