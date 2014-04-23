import os, random, string, json, datetime
from eve import Eve
from auth import AppTokenAuth

current_dir = os.path.dirname(os.path.realpath(__file__))
# The way how Eve looks for the abs settings file would not work when working
# with gunicorn (will look for venv/bin/settings.py). So we provide the abs
# explicitly here. Considering making a PR later.
# https://github.com/nicolaiarocci/eve/blob/develop/eve/flaskapp.py#L171
app = Eve(auth=AppTokenAuth, settings=current_dir+'/settings.py')

def process_client_app_token(request, payload):
  client_id = request.args.get('client_id')
  client_secret = request.args.get('client_secret')

  lookup = { 'client_id': client_id, 'client_secret': client_secret }
  clients = app.data.driver.db['client_apps']
  client = clients.find_one(lookup)

  payload.set_data('{}')
  if client:
    # Ideally, we have to expire tokens periodically and generate new ones.
    # Here we just expire it in 10 years.
    ten_years_from_now = datetime.datetime.now() + datetime.timedelta(days=10*365)
    expires = ten_years_from_now.isoformat()
    data = { u'token': client['token'], u'expires_in': expires }
    payload.set_data(json.dumps(data))

app.on_post_GET_client_apps += process_client_app_token

if __name__ == '__main__':
  port = 5000
  host = '127.0.0.1'

  app.run(host=host, port=port)
