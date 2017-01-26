###############################################################################
# Web Technology at VU University Amsterdam
# Assignment 3
#
# The assignment description is available on Blackboard.
# This is a template for you to quickly get started with Assignment 3. Read
# through the code and try to understand it.
#
# Have you looked at the documentation of bottle.py?
# http://bottle.readthedocs.org/en/stable/index.html
#
# Once you are familiar with bottle.py and the assignment, start implementing
# an API according to your design by adding routes.
###############################################################################

# Include more methods/decorators as you use them
# See http://bottle.readthedocs.org/en/stable/api.html#bottle.Bottle.route
from bottle import response, error, get, post, request, put, delete, abort
import json


###############################################################################
# Routes
#
# TODO: Add your routes here and remove the example routes once you know how
#       everything works.
###############################################################################

@post('/database')
def post_db(db):
    response.content_type = 'application/json' #serve response in json
    
    
    
    #print(request.forms.get('name'))
    #print(request.forms.dict)#here the forms object must be stored in the database.
     
     
    #myDict = request.forms.dict
    myDict = request.json[0]
    #http://stackoverflow.com/questions/9336270/using-a-python-dict-for-a-sql-insert-statement
    #placeholders = ', '.join(['%s'] * len(myDict))
    columns = ', '.join(myDict.keys())
    values = '\', \''.join(myDict.values())
    #flattened_myDict = [item for sublist in myDict.values() for item in sublist]
    #values = ', '.join(flattened_myDict)
    sql = "INSERT INTO inventory ("+columns+") VALUES (\'"+values+ "\' )"
    db.execute(sql)     
     

    return "[{\"action\":\"post\"}]"  

 

@get('/database')
def get_db(db):
    response.content_type = 'application/json'
    
    
    if ('id' in request.params.keys()):
        db.execute('Select * from inventory where id='+request.params['id'])
    else:
        db.execute('Select * from inventory')
    data = db.fetchall()
    response.content_type = 'application/json'
    return json.dumps(data)

@put('/database')
def change_item(db):
    response.content_type = 'application/json' #serve response in json    
    
    myDict = request.json[0]

    if not id_is_present(db, myDict['id']):
        abort(404,"Item with id = "+myDict['id']+' not found.')



    #db.execute('select * from inventory where name='+item_name)
    sql = 'update inventory set name=\''+myDict['name']+'\',category=\''+myDict['category']+'\',amount='+myDict['amount']+',location=\''+myDict['location']+'\',date=\''+myDict['date']+'\' where id='+myDict['id']
    db.execute(sql)
    
    response.status = 204 #Succes, no content
    
    return "[{\"action\":\"update\"}]"  

def id_is_present(db,id_arg):
    sql = 'SELECT 1 FROM inventory WHERE id=\''+id_arg+'\''
    db.execute(sql)
    data = db.fetchall()
    if data:#Data is not empty
        return True
    else:
        return False

 
@delete('/database')
def delete_item(db):
    response.content_type = 'application/json' #serve response in json    
    
    
    
    myDict = request.json[0]

    if not id_is_present(db, myDict['id']):
        abort(404,"Item with id = "+myDict['id']+' not found.')

    sql = 'DELETE FROM inventory WHERE id='+myDict['id']
    db.execute(sql)
    
    response.status = 204 #Succes, no content
    
    return "[{\"action\":\"delete\"}]"  
 
   



###############################################################################
# Error handling
#
# TODO: Add sensible error handlers for all errors that may occur when a user
#       accesses your API.
###############################################################################

@error(404)
def error_404_handler(e):

    # Content type must be set manually in error handlers
    response.content_type = 'application/json'
    
    return json.dumps({'Error': {'Message': response.body, 'Status': e.status_code}})







###############################################################################
# This starts the server
#
# Access it at http://localhost:8080
#
# If you have problems with the reloader (i.e. your server does not
# automatically reload new code after you save this file), set `reloader=False`
# and reload manually.
#
# You might want to set `debug=True` while developing and/or debugging and to
# `False` before you submit.
#
# The installed plugin 'WtPlugin' takes care of enabling CORS (Cross-Origin
# Resource Sharing; you need this if you use your API from a website) and
# provides you with a database cursor.
###############################################################################

if __name__ == "__main__":
    from bottle import install, run
    from wtplugin import WtDbPlugin, WtCorsPlugin

    install(WtDbPlugin())
    install(WtCorsPlugin())
    run(host='localhost', port=8080, reloader=False, debug=True, autojson=False)

