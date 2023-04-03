source flask/bin/activate
export FLASK_DEBUG=0
echo "using $FLASK_ENV server"
flask --app server.py run
