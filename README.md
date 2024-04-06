# ASL Interpretor

This is a work-in-progress project leveraging AI models to translate English to ASL. It does so by first live-transcribing the speaker using Assembly AI, translating English grammar to ASL grammar using OpenAI, then displaying the appropriate set of signs.

## How to run

The first step is to get your OpenAI and AssemblyAI API keys and store them in a file `.env`.

Next, install the required dependencies by running
```
pip install -r requirements.txt
```

Then, to run the live transcriber, simply run:
```
python transcription.py
```

To run the translator, simply go to the notebook `translate.ipynb`, and run the two cells.

To run the ASL animation demo, simply run:
```
python render.py
```