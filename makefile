OUTPUT_DIR=assets
MODEL=models/Llama-3.2-3B-Instruct-Q5_K_M.gguf

AUDIO_MODEL=models/kokoro-v0_19.onnx
VOICE=models/voices.bin
DATE=$(shell date -I)
AUDIO_FILE=$(OUTPUT_DIR)/$(DATE).mp3
TEXT_FILE=$(OUTPUT_DIR)/$(DATE).txt
MD_FILE=$(OUTPUT_DIR)/$(DATE).md
HOME_PAGE=$(OUTPUT_DIR)/index.html
FEED=$(OUTPUT_DIR)/rss.xml
SOURCE_FILE=Morning.ipynb

all: $(AUDIO_FILE) $(MD_FILE) $(TEXT_FILE)

.PHONY: serve

$(MODEL):
	wget "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/$(notdir $(MODEL))" -O $(MODEL)

$(AUDIO_MODEL):
	wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx -P models

$(VOICE):
	wget https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/voices.bin -P models

$(MD_FILE): $(SOURCE_FILE)
	quarto render $(SOURCE_FILE) --to md --execute --output - > $(MD_FILE)

$(TEXT_FILE): $(MD_FILE) $(MODEL)
	python llm.py --model $(MODEL) --input $(MD_FILE) --output $(TEXT_FILE)

$(AUDIO_FILE): $(TEXT_FILE) $(AUDIO_MODEL) $(VOICE)
	python tts.py --input $(TEXT_FILE) --output $(AUDIO_FILE)

serve: all
	./serve
