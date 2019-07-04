from fakenewsdetection import FakeNewDetection # to detect fackeness
from flask import Flask, request, jsonify, abort #to create serve on default port 5000
from flask_cors import CORS , cross_origin #cross origin policy

app = Flask(__name__,static_url_path='/static')
CORS(app)

fake_new_detction_obj = FakeNewDetection()

@app.route('/check-news', methods=['POST'])
def check_news():
    if not request.json:
        abort(400)
    content = request.json
    similarity, sites_url = fake_new_detction_obj.initialize(content['content'])
    print('final similarity is', similarity)
    return jsonify({"similarity":similarity , 'links':sites_url})
    
@app.route('/test')
def test():
    return jsonify({'server':'running'})


if __name__ == '__main__':
	#server ip 127.0.0.1:5000
   app.run(debug=True, host="0.0.0.0")