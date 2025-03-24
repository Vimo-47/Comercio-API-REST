from main import create_app, db
import os

app = create_app()



app.app_context().push()

if __name__ == '__main__':

    db.create_all() #Crea las tablas de la DB

    app.run(port=os.getenv("PORT"), debug=True) #Corre el servidor