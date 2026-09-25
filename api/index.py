import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def proxy_api():
  # Parameters edukkuva, default values-um set cheyyunnu
  types = request.args.get('types', 'telegram')
  key = request.args.get('key', 'lond')
  spell = request.args.get('spell', '')

  # Original render API URL-ilekku request construct cheyyunnu
  backend_url = f'https://rtf-api-server.onrender.com/api?types={types}&key={key}&spell={spell}'

  try:
    response = requests.get(backend_url)
    data = response.json()

    # Response dictionary aanel credits/developer fields remove cheyyuka
    if isinstance(data, dict):
      # Root level-il ulla fields remove cheyyunnu
      keys_to_remove = [
          'credit',
          'credits',
          'tag',
          'tags',
          'developer',
          'owner',
          'author',
          'created_by',
          'DM FOR BUY',
      ]
      for k in keys_to_remove:
        if k in data:
          data.pop(k, None)

      # Result object-inullilum credits/developer undo enn nokki remove cheyyuka
      if 'result' in data and isinstance(data['result'], dict):
        for k in keys_to_remove:
          if k in data['result']:
            data['result'].pop(k, None)
        # Result-il developer tag add cheyyunnu
        data['result']['Developer'] = '@fameneedsme'

      # Root level-ilum developer add cheyyunnu
      data['developer'] = '@fameneedsme'

    return jsonify(data)

  except Exception as e:
    return jsonify({
        'error': True,
        'message': str(e),
        'developer': '@fameneedsme',
    })


@app.route('/', methods=['GET'])
def home():
  return jsonify({
      'status': 'Online',
      'developer': '@fameneedsme',
      'usage': '/api?types=telegram&key=lond&spell=123456789',
  })


if __name__ == '__main__':
  app.run(debug=True)
