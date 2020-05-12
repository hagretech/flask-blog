from flask import Flask , render_template , request ,redirect

app = Flask(__name__)

@app.route('/')
def test():
    return 'hellow world'

if __name__ == '__main__':
    app.run(debug=True)