from blog import create_app
import os
app = create_app()

def getApp():
      return app

if __name__ == '__main__':
      app.run(debug= True, port=8000)