OUTPUT_DIR=assets
DATE=$(shell date -I)
AUDIO_FILE=$(OUTPUT_DIR)/$(DATE).mp3
TEXT_FILE=$(OUTPUT_DIR)/$(DATE).txt
MD_FILE=$(OUTPUT_DIR)/$(DATE).md
HOME_PAGE=$(OUTPUT_DIR)/index.html
FEED=$(OUTPUT_DIR)/rss.xml
MODEL=openrouter/google/gemini-flash-1.5
SOURCE_FILE=Morning.ipynb

all: $(HOME_PAGE) $(FEED)

.PHONY: serve

$(MD_FILE): $(SOURCE_FILE)
	quarto render $(SOURCE_FILE) --to md --execute --output - > $(MD_FILE)

$(TEXT_FILE): $(MD_FILE)
	cat $(MD_FILE) | llm -m $(MODEL) > $(TEXT_FILE)

$(AUDIO_FILE): $(TEXT_FILE)
	edge-tts --file $(TEXT_FILE) --write-media $(AUDIO_FILE)

$(HOME_PAGE) $(FEED): $(AUDIO_FILE) $(TEXT_FILE) $(MD_FILE) templates/index.html gen_rss.py
	python gen_rss.py

serve: $(HOME_PAGE) $(FEED)
	./serve
