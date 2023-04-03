source flask/bin/activate
export FLASK_DEBUG=1
echo "using $FLASK_ENV server"
flask --app server.py --debug run