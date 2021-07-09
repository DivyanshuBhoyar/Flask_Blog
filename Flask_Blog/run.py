from blog import create_app
import os
app = create_app()

def getApp():
      return app

if __name__ == '__main__':
      set_port = os.environ.get('PORT', 8000)
      app.run(debug= True, port=set_port)
