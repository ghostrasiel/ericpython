from flask import Flask , render_template , request

app = Flask(__name__ )
@app.route('/' , methods=['GET' , 'POST'])
def index():
    method = request.method
    name=''
    email=''
    phone=''
    message='' 
    if method == 'POST':
        name = request.form.get('Name')
        email = request.form.get('Email')
        phone = request.form.get('Phone')
        message = request.form.get('Message')

    return render_template('index.html',method=method,name=name , email=email , phone=phone , message=message)
    


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0' , port=5000) #debug在不用重新運行下執行