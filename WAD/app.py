import json
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import datetime
from flask_login import LoginManager, logout_user, login_user, current_user
from flask_login import UserMixin
from flask_login import login_required, logout_user




app = Flask(__name__, static_folder='static')
class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/df1"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY="asdfghjkl"

app.config.from_object(Config)
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    user_id = db.Column(db.VARCHAR(8), unique=True)
    user_password = db.Column(db.VARCHAR(16))

class Topic(db.Model):
    __tablename__ = "topic"

    topic_id = db.Column(db.INT, primary_key=True, autoincrement=True)
    topic_title = db.Column(db.VARCHAR(255), index=True)
    topic_content = db.Column(db.TEXT)
    post_time = db.Column(db.DATETIME, default=datetime.datetime.now())
    user_id = db.Column(db.VARCHAR(8), db.ForeignKey("user.user_id"))
    topics = db.relationship("User", backref="users")
    claims = db.relationship('Claim', back_populates='topic')

class Claim(db.Model):
    __tablename__ = "claim"

    claim_id = db.Column(db.INT, primary_key=True, autoincrement=True)
    claim_title = db.Column(db.VARCHAR(255), index=True)
    topic_id = db.Column(db.INT, db.ForeignKey("topic.topic_id"))
    claim_content = db.Column(db.TEXT)
    post_time = db.Column(db.DATETIME, default=datetime.datetime.now())
    user_id = db.Column(db.VARCHAR(8), db.ForeignKey("user.user_id"))
    topic = db.relationship('Topic', back_populates='claims')
    replys = db.relationship('Reply', backref='reply', cascade='all')

class Reply(db.Model):
    __tablename__ = "reply"

    reply_id = db.Column(db.INT, primary_key=True, autoincrement=True)
    claim_id = db.Column(db.INT, db.ForeignKey("claim.claim_id"))
    reply_content = db.Column(db.TEXT)
    post_time = db.Column(db.DATETIME, default=datetime.datetime.now())
    user_id = db.Column(db.VARCHAR(8), db.ForeignKey("user.user_id"))
    claim = db.relationship('Claim', back_populates='replys')
    rereply_id = db.Column(db.INT, db.ForeignKey("reply.reply_id"))
    replied = db.relationship('Reply', back_populates='replies', remote_side=[reply_id])
    replies = db.relationship('Reply', back_populates='replied', cascade='all')
    retore = None
    reply_claim = None
    reply_reply = None

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ClaimToClaim(db.Model):
    __tablename__ = "claim_claim"

    claim_id = db.Column(db.INT,  primary_key=True)
    claim_id_ = db.Column(db.INT)
    relation_cc = db.Column(db.VARCHAR(10))

class ReplyToClaim(db.Model):
    __tablename__ = "reply_claim"

    reply_id = db.Column(db.INT, primary_key=True)
    claim_id = db.Column(db.INT, )
    relation_rc = db.Column(db.VARCHAR(19))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class ReplyToReply(db.Model):
    __tablename__ = "reply_reply"

    reply_id = db.Column(db.INT, db.ForeignKey("reply.reply_id"), primary_key=True)
    reply_id_ = db.Column(db.INT, db.ForeignKey("reply.reply_id"))
    relation_rr = db.Column(db.VARCHAR(8))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

db.drop_all()
db.create_all()
user1 = User(user_id="Esther", user_password="123456")
db.session.add(user1)
topic1 = Topic(topic_title="Topic1", topic_content="This is topic 1. Topic 1 is a good topic.", user_id="Esther")
topic2 = Topic(topic_title="Topic2", topic_content="This is topic 2. Topic 2 is a good topic, but is different from topic 1.", user_id="Esther")
claim1 = Claim(claim_title="claim1", claim_content="Claim 1 is about claim1.", topic_id=1, user_id="Esther")
claim2 = Claim(claim_title="claim2", claim_content="Claim 2 is about claim2.", topic_id=2, user_id="Esther")
claim3 = Claim(claim_title="claim3", claim_content="Claim 3 is about claim3.", topic_id=1, user_id="Esther")
reply1 = Reply(reply_content='This is a reply', claim_id=1, user_id='Esther')
db.session.add_all([topic1, topic2, claim1, claim2, claim3,reply1])
db.session.commit()


login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
    user = User.query.get(id)
    return user

def to_json(all_vendors):
    v = [ven.to_dict() for ven in all_vendors]
    return v

@app.route('/replyCount/<int:claim_id>/<int:count>', methods=["GET","POST"])
def replyCount(claim_id, count):
    replyList = Reply.query.filter(
        Reply.claim_id == claim_id
    ).all()

    retore = None
    replyToReply = None
    replyToClaim = None
    if len(replyList) == count:
        replyList = None
    else:
        replyList = Reply.query.offset(count).limit(1).all()
        for item in replyList:
            if (item.rereply_id is not None):
                retore = Reply.query.filter(
                    Reply.reply_id == item.rereply_id
                ).first()
                item.retore = retore.to_dict()

                replyToReply = ReplyToReply.query.filter(
                    ReplyToReply.reply_id == item.reply_id,
                    ReplyToReply.reply_id_ == retore.reply_id
                ).first()
                item.reply_reply = replyToReply.to_dict()
            else:
                replyToClaim = ReplyToClaim.query.filter(
                    ReplyToClaim.reply_id == item.reply_id,
                    ReplyToClaim.claim_id == item.claim_id
                ).first()
                item.reply_claim = replyToClaim
    if replyList is None:
        return 'None'
    if retore is not None:
        return jsonify({
            'replyList': to_json(replyList),
            'retore': retore.to_dict(),
            'replyToReply': replyToReply.to_dict(),
        })
    else:
        return jsonify({
            'replyList': to_json(replyList),
            'replyToClaim': replyToClaim.to_dict()
        })

@app.route('/adminLoginUI', methods=["GET","POST"])
def adminLoginUI():
    return render_template("adminLogin.html")


@app.route('/adminTopic', methods=["GET","POST"])
def adminTopic():
    topic_li = Topic.query.all()
    return render_template("adminTopic.html", topic_li=topic_li)


@app.route('/updateTopicData', methods=["GET","POST"])
def updateTopicData():
    data = request.get_data()
    data = json.loads(data)
    topic_id = data.get('topic_id')
    topic_title = data.get('topic_title')
    topic_content = data.get('topic_content')

    topic = Topic.query.filter(
        Topic.topic_id == topic_id
    ).first()
    topic.topic_title = topic_title
    topic.topic_content = topic_content
    db.session.commit()
    return {
        'topic_title': topic_title,
        'topic_content': topic_content
    }



@app.route('/delTopic', methods=["GET","POST"])
def delTopic():
    topic_id = request.args.get('topic_id')
    topic = Topic.query.filter(
        Topic.topic_id == topic_id
    ).first()
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('adminTopic'))


@app.route('/adminClaim', methods=["GET","POST"])
def adminClaim():
    claim_li = Claim.query.all()
    return render_template("adminClaim.html", claim_li=claim_li)


@app.route('/delclaim', methods=["GET","POST"])
def delclaim():
    claim_id = request.args.get('claim_id')
    claim = Claim.query.filter(
        Claim.claim_id == claim_id
    ).first()
    db.session.delete(claim)
    db.session.commit()
    return redirect(url_for('adminClaim'))

@app.route('/updateClaimData', methods=["GET","POST"])
def updateClaimData():
    data = request.get_data()
    data = json.loads(data)
    claim_id = data.get('claim_id')
    claim_title = data.get('claim_title')
    claim_content = data.get('claim_content')

    claim = Claim.query.filter(
        Claim.claim_id == claim_id
    ).first()
    claim.claim_title = claim_title
    claim.claim_content = claim_content
    db.session.commit()
    return {
        'claim_title': claim_title,
        'claim_content': claim_content
    }


@app.route('/adminReply', methods=["GET","POST"])
def adminReply():
    reply_li = Reply.query.all()
    return render_template("adminReply.html", reply_li=reply_li)

@app.route('/updateReplyData', methods=["GET","POST"])
def updateReplyData():
    data = request.get_data()
    data = json.loads(data)
    reply_id = data.get('reply_id')
    reply_content = data.get('reply_content')

    reply = Reply.query.filter(
        Reply.reply_id == reply_id
    ).first()
    reply.reply_content = reply_content
    db.session.commit()
    return {
        'reply_content': reply_content
    }



@app.route('/delReply', methods=["GET","POST"])
def delReply():
    reply_id = request.args.get('reply_id')
    reply = Reply.query.filter(
        Reply.reply_id == reply_id
    ).first()
    db.session.delete(reply)
    db.session.commit()
    return redirect(url_for('adminReply'))


@app.route('/adminLogin', methods=["GET","POST"])
def adminLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(
        User.user_id == username,
        User.user_password == password
    ).first()
    if (user is not None and user.user_id == 'admin'):
        return redirect(url_for('adminClaim'))
    return render_template("adminLogin.html", msg='Username Or Password Error')




@app.route('/', methods=["GET","POST"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        if form.Register.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                return redirect(url_for('index'))
            else:
                user = User(user_id=name, user_password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
        elif form.Login.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                if name == user.user_id and password == user.user_password:
                    login_user(user)  # 登入用户
                    flash('Login success.')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password.')
                    return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('index'))
    if request.args.get('search'):
        return redirect(url_for('search'))
    if request.args.get('logout'):
        return redirect(url_for('logout'))
    topic_li = Topic.query.all()
    return render_template("index.html", topics=topic_li, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/<int:topic_id>', methods=["GET","POST"])
def topic(topic_id):
    form = UserForm()
    if form.validate_on_submit():
        if form.Register.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                return redirect(url_for('index'))
            else:
                user = User(user_id=name, user_password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
        elif form.Login.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                if name == user.user_id and password == user.user_password:
                    login_user(user)  # 登入用户
                    flash('Login success.')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password.')
                    return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('index'))
    sort = request.args.get('sort')
    if (sort is None):
        topic = Topic.query.get(topic_id)
        claim_li = Claim.query.all()
    else:
        if (sort == 'True'):
            topic = Topic.query.get(topic_id)
            claim_li = Claim.query.order_by(Claim.post_time.desc()).all()
            sort = 'False'
        else:
            topic = Topic.query.get(topic_id)
            claim_li = Claim.query.order_by(Claim.post_time.asc()).all()
            sort = 'True'
    print(sort)

    return render_template("Topic_page.html", topic=topic, claims=claim_li, form=form, sort=sort)

@app.route('/write_topic', methods=["GET","POST"])
def write_topic():
    if request.method == 'POST':
        user = current_user._get_current_object()
        title = request.form.get('tname')
        desc = request.form.get('tdesc')
        if not title or not desc:
            flash('Invalid input')
        topic = Topic(topic_title=title, topic_content=desc, user_id=user.user_id)
        db.session.add(topic)
        db.session.commit()
        flash('Successfully!')
        return redirect(url_for('index'))
    return render_template("Write_topic.html")

@app.route('/claim/<int:claim_id>', methods=["GET","POST"])
def claim(claim_id):
    form = UserForm()
    if form.validate_on_submit():
        if form.Register.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                return redirect(url_for('index'))
            else:
                user = User(user_id=name, user_password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
        elif form.Login.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                if name == user.user_id and password == user.user_password:
                    login_user(user)  # 登入用户
                    flash('Login success.')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password.')
                    return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('index'))
    if request.args.get('rereply'):
        replied_id = request.args.get('reply')
        if replied_id:
            rereply=Reply.query.get(replied_id)
            reply.replied=rereply
    claim = Claim.query.get(claim_id)

    claimToClaim =  ClaimToClaim.query.filter(
        ClaimToClaim.claim_id == claim_id
    ).first()
    relClaimClaim = None
    if (claimToClaim is not None):
        relClaimClaim = Claim.query.get(claimToClaim.claim_id_)

    topic_id = claim.topic_id
    topic = Topic.query.get(topic_id)
    # Comment
    reply_li = Reply.query.all()
    sort = request.args.get('sort')
    if (sort == 'True'):
        reply_li = Reply.query.order_by(
            Reply.post_time.desc()
        ).all()
        for item in reply_li:
            if (item.rereply_id is not None):
                retore = Reply.query.filter(
                    Reply.reply_id == item.rereply_id
                ).first()
                item.retore = retore

                replyToReply = ReplyToReply.query.filter(
                    ReplyToReply.reply_id == item.reply_id,
                    ReplyToReply.reply_id_ == retore.reply_id
                ).first()
                item.reply_reply = replyToReply
            else:
                replyToClaim = ReplyToClaim.query.filter(
                    ReplyToClaim.reply_id == item.reply_id,
                    ReplyToClaim.claim_id == claim_id
                ).first()
                item.reply_claim = replyToClaim
            sort = 'False'
    else:
        reply_li = Reply.query.order_by(
            Reply.post_time.asc()
        ).all()
        for item in reply_li:
            if (item.rereply_id is not None):
                retore = Reply.query.filter(
                    Reply.reply_id == item.rereply_id
                ).first()
                item.retore = retore

                replyToReply = ReplyToReply.query.filter(
                    ReplyToReply.reply_id == item.reply_id,
                    ReplyToReply.reply_id_ == retore.reply_id
                ).first()
                item.reply_reply = replyToReply
            else:
                replyToClaim = ReplyToClaim.query.filter(
                    ReplyToClaim.reply_id == item.reply_id,
                    ReplyToClaim.claim_id == claim_id
                ).first()
                item.reply_claim = replyToClaim
        sort = 'True'

    return render_template("Claim_page.html", claim=claim, topic=topic, replys=reply_li, form=form, sort=sort, claimToClaim=claimToClaim,relClaimClaim=relClaimClaim)

@app.route('/write_claim/<int:topic_id>', methods=["GET","POST"])
def write_claim(topic_id):

    topic = Topic.query.get(topic_id)
    if request.method == 'POST':
        user = current_user._get_current_object()
        title = request.form.get('tname')
        desc = request.form.get('tdesc')
        claim_id_ = request.form.get('r1_')
        relation_cc = request.form.get('r1')
        if not title or not desc:
            flash('Invalid input')
            return redirect(url_for('write_claim',topic_id=topic.topic_id))
        claim = Claim(claim_title=title, claim_content=desc, user_id=user.user_id, topic_id=topic.topic_id)
        db.session.add(claim)
        db.session.commit()
        claim_id = claim.claim_id
        recc = ClaimToClaim(claim_id=claim_id, claim_id_=claim_id_, relation_cc=relation_cc)
        db.session.add(recc)
        db.session.commit()
        flash('Successfully!')
        return redirect(url_for('topic', topic_id=topic.topic_id))
    claim_li = Claim.query.all()
    return render_template("Write_claim.html", topic=topic, claim_li=claim_li)

@app.route('/reply/<int:claim_id>', methods=["GET","POST"])
def reply(claim_id):
    claim = Claim.query.get(claim_id)
    topic_id = claim.topic_id
    if request.method == 'POST':
        user = current_user._get_current_object()
        desc = request.form.get('tdesc')
        if not desc:
            flash('Invalid input')
            return redirect(url_for('claim', claim_id=claim.claim_id))
        reply = Reply(reply_content=desc, claim_id=claim_id, user_id=user.user_id)
        db.session.add(reply)

        db.session.flush()

        category = request.form.get('category')
        if category == 'Claim':
            relation_rc = request.form.get('relation_rc')
            replyToClaim = ReplyToClaim(reply_id=reply.reply_id, claim_id=claim_id, relation_rc=relation_rc)
            db.session.add(replyToClaim)

        db.session.commit()
        flash('Successfully!')
        return redirect(url_for('claim', claim_id=claim.claim_id))
    return render_template("Reply_page.html", claim=claim, topic=topic)

@app.route('/reply/rereply/<int:reply_id>', methods=["GET","POST"])
def rereply(reply_id):
    reply = Reply.query.get(reply_id)
    claim_id = reply.claim_id
    claim = Claim.query.get(claim_id)

    if request.method == 'POST':
        user = current_user._get_current_object()
        desc = request.form.get('tdesc')
        parentId = request.form.get('parentId')
        if not desc:
            flash('Invalid input')
            return redirect(url_for('claim', claim_id=claim.claim_id))
        reply = Reply(reply_content=desc, claim_id=claim_id, user_id=user.user_id, rereply_id=parentId)
        db.session.add(reply)
        db.session.flush()

        category = request.form.get('category')
        # if category == 'Claim':
        #     relation_rc = request.form.get('relation_rc')
        #     replyToClaim = ReplyToClaim(reply_id=reply.reply_id, claim_id=claim_id, relation_rc=relation_rc)
        #     db.session.add(replyToClaim)
        if category == 'Reply':
            relation_rr = request.form.get('relation_rr')
            replyToReply = ReplyToReply(reply_id=reply.reply_id, reply_id_=reply_id, relation_rr=relation_rr)
            db.session.add(replyToReply)
        db.session.flush()
        db.session.commit()

        flash('Successfully!')
        return redirect(url_for('claim', claim_id=claim.claim_id))
    return render_template("Reply_page.html", claim=claim, topic=topic,reply=reply)

@app.route('/user', methods=["GET","POST"])
def user():
    id = request.args.get('id')
    user = User.query.get(id)
    return render_template("user.html", user=user)

@app.route('/search', methods=["GET","POST"])
def search():
    form = UserForm()
    if form.validate_on_submit():
        if form.Register.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                return redirect(url_for('index'))
            else:
                user = User(user_id=name, user_password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
        elif form.Login.data:
            name = form.name.data
            password = form.password.data
            user = User.query.filter(
                User.user_id == name,
                User.user_password == password
            ).first()
            if (user is not None):
                if name == user.user_id and password == user.user_password:
                    login_user(user)  # 登入用户
                    flash('Login success.')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password.')
                    return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('index'))

    # keyword = request.form.get('keywords')

    value = request.form.get('keywords')
    if (value is None):
        return render_template("Search.html", form=form)
    result = db.session.query(Topic).filter(Topic.topic_title.like('%'+value+'%')).all()
    result = db.session.query(Topic).filter(Topic.topic_title.like('%' + value + '%')).all()
    result2 = db.session.query(Claim).filter(Claim.claim_title.like('%' + value + '%')).all()
    result3 = db.session.query(Claim).filter(Claim.claim_content.like('%' + value + '%')).all()
    return render_template("Search.html", form=form, results = result, results2 = result2, results3 = result3)


# Log in table
class UserForm(FlaskForm):
     name = StringField(label=u"", id="", validators=[DataRequired(u"Must be filled...")])
     password = StringField(label=u"", id="", validators=[DataRequired(u"Less than 16 digits")])
     Login = SubmitField(id="loginButton")
     Register= SubmitField(id="registerButton")


if __name__ == '__main__':
    app.run(debug=True)
    # db.drop_all()
    # db.create_all()
    # user2 = User(user_id="Kirk", user_password="123456")
    # db.session.add(user2)
    # db.session.commit()
    # topic = Topic(topic_title="Topic1")
    # user1 = User(user_id="Esther") #插入数据
    # db.session.add(user1)
    # db.session.add_all([user1, user2])
    # db.session.commit()