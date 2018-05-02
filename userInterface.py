from flask import Flask, render_template, request

import search
app = Flask(__name__, static_url_path = "/Images", static_folder = "Images")
app.debug = True

@app.route('/')
def student():
   return render_template('hello.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
        if request.method == 'POST':
            print("This is the user value :  ", request.get_data());
            search.search_query((request.get_data()).decode("utf-8") )
            return render_template('results.html')


