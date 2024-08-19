import logging
from flask import Flask, request, render_template, send_from_directory, url_for, redirect
# Load model directly
from transformers import AutoProcessor, MusicgenForConditionalGeneration, AutoModel
import torch
device = "cuda:0" if torch.cuda.is_available() else "cpu"
import scipy
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
sampling_rate = model.config.audio_encoder.sampling_rate
processor1 = AutoProcessor.from_pretrained("suno/bark-small")
model1 = AutoModel.from_pretrained("suno/bark-small").to(device)
sampling_rate1 = model1.generation_config.sample_rate

logging.basicConfig(format='日志%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.INFO)

# flask 函数
app = Flask(__name__)
@app.route("/")
def get_prompt():
    return render_template("getprompt.html")
@app.route("/ready/", methods=["GET"])
def app_ready():
    logging.info("ready")
    return {"ready":"true"}
 
@app.route("/api/app/generate/", methods=["POST"])
def app_generate():
    logging.info('开始生成')
    print(request.form)
    prompt = request.form['prompt']
    logging.info("test")
    make_instrumental = request.form['make_instrumental']== "true"
    tags = request.form['tags']
    
    length = request.form['length']

    length = int(length)
    max_new_tokens = length * model.config.audio_encoder.frame_rate
    audio_filename = "musicgen_out.wav"
    if make_instrumental==False:
        prompt = "♪"+prompt+"♪"
        input = processor1(prompt)
        audio_values = model1.generate(**input.to(device))
        scipy.io.wavfile.write(audio_filename, rate=sampling_rate1, data=audio_values[0].cpu().numpy())
    else:
        input = processor(text = tags+prompt,return_tensors = "pt")
        audio_values = model.generate(**input.to(device), max_new_tokens=max_new_tokens)
        scipy.io.wavfile.write(audio_filename, rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
    
    logging.info('生成成功!')
    return redirect(url_for('musicplay', filename = audio_filename))

@app.route("/musicplay/<path:filename>")
def musicplay(filename):
    return send_from_directory("./",filename)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 80,debug=True)