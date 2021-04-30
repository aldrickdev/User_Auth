from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth.auth import AuthHandler
from models.schemas import AuthDetails
import uvicorn


app: FastAPI = FastAPI()
app.mount('/static', StaticFiles(directory='../../frontend/build/static'), name='static')
templates = Jinja2Templates(directory="../../frontend/build")


# Database
users = []
auth_handler = AuthHandler()

@app.get('/', response_class=HTMLResponse, status_code=200)
def index(request: Request):
  return templates.TemplateResponse("index.html", {"request":request})
 
@app.post('/login')
def login(auth_details: AuthDetails):
  user = None
  for u in users:
    if u['username'] == auth_details.username:
      user = u
      break

  if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
    raise HTTPException(status_code=401, detail='Invalid Username or Password')

  token = auth_handler.encode_token(user['username'])
  return {
    'message':f'{auth_details.username} has logged in',
    'token': token
    }
 
@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
  # Checks to see if is taken
  if any(user['username'] == auth_details.username for user in users):
    raise HTTPException(status_code=400, detail='Username is Taken')

  hashed_password = auth_handler.get_password_hash(auth_details.password)
  users.append({
    'username':auth_details.username,
    'password':hashed_password
  })
  return {'message':f'User Created {auth_details.username}'}

@app.get('/dashboard')
def dashboard():
  usernames = []
  [usernames.append(user['username']) for user in users]
  payload = {
    "users":usernames
  }
  return payload

@app.get('/delete')
def delete(username=Depends(auth_handler.auth_wrapper)):
  for index, user in enumerate(users):
    if user['username'] == username:
      del users[index]
  return {'Delete': username}

def main():
  print('Starting App')
  uvicorn.run(app=app, port=8001, host='127.0.0.1')

if __name__ == '__main__':
  main()
else:
  main()