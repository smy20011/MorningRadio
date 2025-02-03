# Morning Radio - Locally Generated Personal Morning Broadcast

Morning Radio is a set of Python scripts that allows you to generate a personalized broadcast for your morning commute. You write a script using a Jupyter Notebook, and it uses a local LLM to generate the script and a local TTS system to synthesize it into audio.

It also ships with a podcast server and a scheduling system that automatically creates the podcast at 7:30 AM your local time.

## How to Run

Before running the script, make sure you have GCC and Make installed on your system.

### Run with UV

[UV](https://github.com/astral-sh/uv) is recommended for running the system. It makes package installation much easier. To run the entire system (including the podcast server), use:

```
uv run make serve
```

UV will install the packages, create the virtual environment, and run the command within the virtual environment. The script will download the model files and start generation. After generation is finished, a server will be running at localhost:5000 with a list of generated podcasts.

### Run with Virtual Environment

We also provide a `requirements.txt` file for you to install packages in a virtual environment. In a virtual environment, use:

```
pip install -r requirements.txt
make serve
```

to start the broadcast generation and podcast server.

### Connect to Podcast App

Once generated, the podcast will be available on the local network. However, if you want to listen to the podcast from a remote location, you need to either:

1. Expose port 5000 to the public network and ensure you have a static IP address.
2. Use a VPN (like [Tailscale](https://tailscale.com/)) to connect to your podcast host.

I use the second option since it's easier and more secure.


## Customization

This project is meant to be forked and modified to fit your needs.

### Customize Broadcast Content

Change the `Morning.ipynb` file to change the content of the broadcast. You can add any cell to change the content. You can use print statements to print the prompt you want to send to the LLMs, for example, adding a cell with:

```python
print("Hello Foo")
```

will add "Hello Foo" to the prompt being sent to the LLM.

Morning Radio uses Quatro to convert the `.ipynb` file to Markdown format. See the [Quatro](https://quarto.org/) website for more information.

### Customize LLM Script Generation

I use LLAMA 3b to convert the output of the `.ipynb` file to the broadcast script. To use a more advanced model or a non-local model, you can change the Makefile, pointing the model to a new location. `$(MODEL)` needs to be a model in GGUF format.

```makefile
$(TEXT_FILE): $(MD_FILE) $(MODEL)
        python llm.py --model $(MODEL) --input $(MD_FILE) --output $(TEXT_FILE)
```

To change model parameters, you can change `llm.py`. I use the `llama_cpp` Python package to run the local model. Please refer to the `llama_cpp` documentation for customization tips.

### Customize Audio Generation

I use Kokoro to convert text to audio. To customize the voice or speed, change `tts.py` to fit your needs.
