from auto_complete import AutoCompleteModel
import glob


def test_single_train():
	data = ""

	for filename in glob.glob("lyrics/*.txt")[:10]:
		with open(filename, "r") as f:
			data += f.read()
			data += "\n"

	model = AutoCompleteModel()
	model.build_model(data)
	model.save_model("model.pkl")
	model.load_model("model.pkl")

	single_words_pool = model.get_single_words_pool()
	tuple_words_pool1 = model.get_tuple_words_pool()
	print(single_words_pool)
	print(tuple_words_pool1)


def test_incremental_train():
	model = AutoCompleteModel(chunk_size=2)

	for filename in glob.glob("lyrics/*.txt"):
		with open(filename, "r") as f:
			data = f.read()
			model.build_model(data, incremental=True)

	single_words_pool = model.get_single_words_pool()
	tuple_words_pool = model.get_tuple_words_pool()

	# print(single_words_pool1 == single_words_pool)
	# print(tuple_words_pool1==tuple_words_pool)


model = AutoCompleteModel(chunk_size=2)

for filename in glob.glob("lyrics/*.txt"):
	with open(filename, "r") as f:
		data = f.read()
		model.build_model(data, incremental=True)

# model.save_model("model_6singers.pkl")
model.load_model("model_6singers.pkl")

# w1 = model.generate_random_word()
# w2 = model.generate_next_word(w1)
# print(model.generate_one_sentence(limit_size=4))

print(model.generate_sentences(num_of_sentence=8, limit_word_size=4))
