from flaskblog import create_app

# Create the Flask application instance using the factory function
app = create_app()
#Runing the app like regular python file
if __name__ =='__main__':
    app.run(debug=True)
    