from fastapi import FastAPI

# class App:
#   def __init__(self, app):
#     print('Created App')

# Database
users = []

app: FastAPI = FastAPI()
@app.get('/')
def index():
  return {'Hello': 'World'}

@app.post('/login')
def login():
  return {'Page': 'Login'}

@app.post('/register')
def register():
  return {'Page': 'Register'}

@app.get('/dashboard')
def dashboard():
  return {'Page': 'Dashboard'}

@app.delete('/delete')
def delete():
  return {'Page': 'Delete'}

def main():
  print('Starting App')

if __name__ == '__main__':
  main()