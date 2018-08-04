from flask import Flask, render_template, request
from peewee import *
import datetime
from os import path


flaskapp = Flask(__name__) #instantialize the Flask class
flaskapp._static_folder = path.abspath("static")


db = SqliteDatabase('posts.db') #Set our database type and file for peewee

#define some data models, post and postreply
class Post(Model):
	title = CharField()
	content = CharField()
	
	class Meta:
		database = db
	
class PostReply(Model):
	content = CharField()
	replyTo = IntegerField()
	owner = CharField()
	class Meta:
		database = db
		
db.connect() #pre-emptively connect for early error detection
db.create_tables([Post,PostReply]) #create our tables
	
@flaskapp.route('/', methods=['POST','GET']) #let's route / to a home page listing posts
def load_posts():
	try:
		leposts = Post.select()
		if request.method == "POST":
			newpost = Post.create(title=request.form.get('post_title'), content = request.form.get('postbody'))
		return render_template('home.html',posts=leposts)
	except:
		return render_template('home.html')
@flaskapp.route('/posts/<postid>', methods=['POST', 'GET'])
def load_post_page(postid):
	try:
		myreplies = PostReply.select().where(PostReply.replyTo == postid)
		mypost = Post.select().where(Post.id == postid).get()
	except: 
		return render_template('404.html')
	if request.method == "POST":
		newreply = PostReply.create(content=request.form.get('responsebody'),owner = request.form.get('myname'),replyTo = postid)
	#for xx in mypost:
	#	print(xx)
	return render_template('postthread.html', post=mypost,replies=myreplies)
	