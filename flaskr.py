from flask import Flask, jsonify, render_template, request
from flask_bootstrap import Bootstrap
import biligrab
import os

app = Flask(__name__)
Bootstrap(app)

def getChromecast():
	chromecasts = pychromecast.get_chromecasts()
	return chromecasts[0]

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/getData")
def getData():
	url = request.args.get('url')
	title,aid,img=biligrab.getAid(url)
	ret=biligrab.getCid(aid)
	for r in ret:
		r['title']=title
		r['img']=img
	return jsonify(ret)

@app.route("/getUrl")
def getUrl():
	cid=request.args.get('cid')
	return jsonify(biligrab.get_media_urls(cid))
	
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0',port=port);