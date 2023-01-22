from flask import Flask, render_template, session, redirect, request, jsonify
# from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from flask_bcrypt import Bcrypt
from forms import AddUserForm, LoginForm, Add_New_Feedback, Edit_Feedback, Delete
# from serialized import seririalized
# import datetime

app = Flask(__name__)


app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_authentication'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'cows'
# DEBUG_TB_INTERCEPT_REDIRECTS = False
# toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()

bcrypt = Bcrypt()



@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        print(f'''
        
        ****************************************
        username: {username}
        password: {password}
        email: {email}
        First name: {first_name}
        Last name: {last_name}
        ****************************************

        ''')
        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode("utf8")
        # User.register(username, password)

        # print([username, password, email])
        new_user = User(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        signed_in_user = User.query.filter_by(username=username).first()
        session['user_id'] = signed_in_user.id
        session['username'] = signed_in_user.username
        # flash(f"Added {name} at {price}")
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    try:
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            u_name = User.query.filter_by(username=username).first()
            print(f'''
        
            {u_name.password}
        
            ''')
        # hashed_password = bcrypt.generate_password_hash(password)
        # authenticated_password = User.authenticate(username, password)

            auth_pass = bcrypt.check_password_hash(u_name.password, password=password)
            print(f'''
        
            {auth_pass}
        
            ''')
        
            if auth_pass == True:
                session['user_id'] = u_name.id
                session['username'] = u_name.username
                return redirect('/secret')
        # flash(f"Added {name} at {price}")
        # if authenticated_password == False:
        # #     return redirect('/login')
            else:
                return redirect('/login')
    except:
        return redirect('/login')


    else:
        return render_template("register.html", form=form)

@app.route('/secret')
def secret():
    
    try:
        if 'user_id' in session:
            return render_template('/secret.html', username=session['username'])
        else:
            return redirect('/')    
    except:
        return redirect('/')

@app.route('/logout')
def logout():
    try:
        session.pop('user_id')
        session.pop('username')
        print(f'''
    ####################################################################################################################################
                                            {session['user_id']} / {session['username']}
    ####################################################################################################################################
    ''')
        return redirect('/login')
    except:
        return redirect('/login')
@app.route('/users/<username>')
def user_profile(username):
    current_user = User.query.filter_by(username=username).first()
    print(current_user)
    users_feedback = Feedback.query.filter_by(username=username)

    return render_template('user_page.html', username=session['username'], C_U=current_user, U_F=users_feedback)


####################################################################################################################################
# Second Wave:

@app.route('/users/<username>/delete', methods=['POST', 'GET'])
def delete_user(username):
    form = Delete()
    if form.validate_on_submit():
        post = form.delete_post.data
        if post == True:
            feedback_for_delete = Feedback.query.filter_by(username=username).all()
            user_for_delete = User.query.filter_by(username=username).first()
            for dp in feedback_for_delete:
                db.session.delete(dp)
            
            
            db.session.delete(user_for_delete)
            db.session.commit()
            session.pop('username')
            session.pop('user_id')
            

            return redirect('/register')



    return render_template('register.html', form=form)
    
@app.route('/users/<username>/feedback/add', methods=['POST', 'GET'])
def new_feedback(username):
    form = Add_New_Feedback()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        print(f'''
        
        *****************************************************************************
        
        Title: {title}
        Content: {content}
        Username: {username}

        *****************************************************************************
        ''')
        
        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)
    
# @app.route('/users/<username>/feedback/add')
# def new_feedback(username):
#     return 'Add More Feedback'

@app.route('/feedback/<feedback_id>/update', methods=['POST', 'GET'])
def update_feedback(feedback_id):
    single_feedback = Feedback.query.get(feedback_id)
    form = Edit_Feedback()
    
    # curr_user = User.query.filter_by()
    try:
        if session['username'] != single_feedback.username:
            return redirect(f'/users/{session["username"]}')
    except:
        return redirect('/login')
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        deleting = form.deleting.data
        print(f'''******************************************************
                        {title} / {content}
                 ******************************************************
        ''')
        if title != "":
            single_feedback.title = title
            # return single_feedback
        if content != "":
            single_feedback.content = content
            # return single_feedback
        db.session.add(single_feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')


    return render_template('feedback_post_page.html', fb=single_feedback, form=form)

@app.route('/feedback/<feedback_id>/delete', methods=['POST', 'GET'])
def delete_feedback(feedback_id):
    form = Delete()
    if form.validate_on_submit():
        post = form.delete_post.data
        deleting_post = Feedback.query.get(feedback_id)
        if post == True:
            db.session.delete(deleting_post)
            db.session.commit()
            
            # Feedback.query.filter_by(id=feedback_id).first().delete()

        return redirect(f'/users/{session["username"]}')
    

    
    return render_template('register.html', form=form)

