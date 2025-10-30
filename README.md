# LLM RAG Bot Project
We are developing a Discord Bot, integrating LLM and RAG capabilities. We will be using the [Pycord](https://pycord.dev/) library to develop the Discord Bot. We will also be using [ChromaDB](https://docs.trychroma.com/docs/overview/introduction) as our vector database for RAG capabilities.

The LLM will be ran locally, using [KoboldCPP](https://github.com/LostRuins/koboldcpp). The model that we are choosing is a Mistral 7b Q4_K_M base model which can be found here: https://huggingface.co/MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF.

We will be using a few of their endpoints, as well as their websearch endpoint to easily use search results to store in the vector database.

## Setup

### Python  
For this project, we will be using Python 3.10.11. You can download and install that here: https://www.python.org/downloads/release/python-31011/  

### Virtual Environment
Set up uv, a modern and fast Python package manager: https://docs.astral.sh/uv/getting-started/installation/  

Then in your terminal, navigate to the project's root directory, and enter:  
`uv venv`  

You should now have created a virtual environment. Activate the virtual environment and enter:  
`uv pip install -r requirements.txt`  

### Project Secrets
You will need to create a .env file. This will hold the Discord Bot's token needed for our application. You may ask Brian to give you the Discord Bot token.  

### Contributions
When contributing or adding features, please create a branch and make your changes. Then submit a Pull Request.
