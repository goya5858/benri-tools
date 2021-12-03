from fastapi import FastAPI
import onnxruntime as ort 

app = FastAPI(title="MLOps sample")

class ONNXModel:
    def __init__(self):
        onnx_model_path = "models/SampleModel.onnx"
        self.ort_session = ort.InferenceSession( onnx_model_path )

    def predict(self, inp):
        # Inputの名前を、モデルの変換時のものと一致させる
        ort_inputs = { "input": inp } 
        onnx_pred = self.ort_session.run( None, ort_inputs )[0]
        # Noneで、モデルのすべてのOutputを取得する
        # Noneではなく、ONNX変換時に指定したoutput名を入れればそれを取得可能
        return onnx_pred

@app.get("/")
async def home_page():
    return "<h2>Sample prediction API</h2>"

@paa.get("/predict")
async def get_prediction(nums: str):
    inputs = [[float(n) for n in nums.split(" ") ]]
    model = ONNXModel()
    pred = model.predict(inputs)
    return pred