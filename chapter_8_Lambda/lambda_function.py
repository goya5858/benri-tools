import json
import onnxruntime as ort 

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

def lambda_handler(event, context):
    model = ONNXModel()
    if "resource" in event.keys():
        body = event["body"]
        body = json.loads(body)
        print(f"Got the input: {body['sentence']}")
        response = model.predict(body["sentence"])
        return {
			"statusCode": 200,
			"headers": {},
			"body": json.dumps(response)
		}
    else:
        return model.predict(event["sentence"])