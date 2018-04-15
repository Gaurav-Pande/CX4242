from flask import Flask, render_template, request, json, redirect

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/Test')
def test():
	return redirect("http://www.bilibili.com")

@app.route('/SignUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

if __name__=="__main__":
    app.run()
