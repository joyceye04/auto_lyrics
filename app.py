from auto_complete import AutoCompleteModel

import json
from flask import Flask, request, jsonify
app = Flask(__name__)


global model 

model = AutoCompleteModel(chunk_size=2)


@app.route("/activate", methods=["POST"])
def init():
	json_input = json.loads(request.get_data())
	configs = json_input.get("configs")
	print(configs)
	model_name = configs.get("model_name", "model_lyrics")
	try:
		model.load_model("model_saved/{}.pkl".format(model_name))
		return json.dumps("SUCCESS"), 200, {'content-type':'application/json'}
	except:
		return json.dumps("FAIL"), 500, {'content-type':'application/json'}


@app.route("/compose", methods = ["POST"])
def compose():
	json_input = json.loads(request.get_data())
	configs = json_input.get("configs")
	print(configs)
	num_of_sentence = configs.get("num_of_sentence", 4)
	limit_word_size = configs.get("limit_word_size", 4)
	
	re = dict()
	try:
		lyrics = model.generate_sentences(num_of_sentence=num_of_sentence, limit_word_size=limit_word_size)
		re.update({"response": lyrics})
		return json.dumps(re), 200, {'content-type':'application/json'}
	except:
		re.update({"response": "model server error"})
		return json.dumps(re), 500, {'content-type':'application/json'}


app.run(host='0.0.0.0', port=8080)
