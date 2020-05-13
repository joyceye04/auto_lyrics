from auto_complete import AutoCompleteModel
import glob


data = ""

for filename in glob.glob("lyrics/*.txt")[:10]:
    with open(filename, "r") as f:
        data += f.read()
        data += "\n"


model = AutoCompleteModel()
model.build_model(data)
model.save_model("model.pkl")