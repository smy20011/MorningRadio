OUTPUT_DIR=assets
DATE=$(shell date -I)
AUDIO_FILE=$(OUTPUT_DIR)/$(DATE).mp3
TEXT_FILE=$(OUTPUT_DIR)/$(DATE).txt
MD_FILE=$(OUTPUT_DIR)/$(DATE).md
MODEL=openrouter/google/gemini-flash-1.5
SOURCE_FILE=Morning.ipynb

$(AUDIO_FILE) $(TEXT_FILE) $(MD_FILE): $(SOURCE_FILE)
	quarto render $(SOURCE_FILE) --to md --execute --output - > $(MD_FILE)
	cat $(MD_FILE) | llm -m $(MODEL) > $(TEXT_FILE)
	edge-tts --file $(TEXT_FILE) --write-media $(AUDIO_FILE)
