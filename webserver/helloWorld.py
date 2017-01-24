from bottle import route, run, template, request

@route('/')
@route('/hello/<name>')
def greet(name='Stranger'):
    return template('Hello {{name}}, how are you?', name=name)

@route('/hello')
def hello():
    name = request.cookies.username or 'Guest'
    return template('Hello {{name}}', name=name)

from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry2'

run(host='localhost', port=8080, debug=True, reloader=True)