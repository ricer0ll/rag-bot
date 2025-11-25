# LLM RAG Bot Project
We are developing a Discord Bot, integrating LLM and RAG capabilities. We will be using the [Pycord](https://pycord.dev/) library to develop the Discord Bot. We will also be using [ChromaDB](https://docs.trychroma.com/docs/overview/introduction) as our vector database for RAG capabilities.

The LLM will be ran locally, using [KoboldCPP](https://github.com/LostRuins/koboldcpp). The model that we are choosing is a Mistral 7b Instruct Q4_K_M base model which can be found here: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF.

# Development Setup

### Python  
For this project, we will be using Python 3.10.11. You can download and install that here: https://www.python.org/downloads/release/python-31011/  

### Virtual Environment
Set up uv, a modern and fast Python package manager: https://docs.astral.sh/uv/getting-started/installation/  

Then in your terminal, navigate to the project's root directory, and enter:  
`uv venv --python 3.10`  

You should now have created a virtual environment. Activate the virtual environment and enter:  
`uv pip install -r requirements.txt`  

### Project Secrets
You will need to create a .env file. This will hold the Discord Bot's token needed for our application.
```
DISCORD_TOKEN=abcdefg12345
ENVIRONMENT=DEV
```

If you are deploying the bot using Docker, please set `ENVIRONMENT=PROD` in your Docker env file.  

### Running the Discord Bot
Simply run:  
`python main.py`


# Docker Deployment
For ease of deployment, we also provide a docker-compose to deploy and run the bot:
```
services:
  rag-bot:
    image: ricer0ll/rag-bot
    container_name: rag-bot
    user: "1001:100"
    ports:
      - "8000:8000"
    volumes:
      - /srv/dev-disk-by-uuid-e63447d1-8e01-4c42-a96e-1760332fccef/data/appdata:/app/data
      - /srv/dev-disk-by-uuid-e63447d1-8e01-4c42-a96e-1760332fccef/data/appdata/.cache:/app/.cache
    environment:
      - TRANSFORMERS_CACHE=/app/.cache
      - HF_HOME=/app/.cache
      - TORCH_HOME=/app/.cache
    env_file:
      - rag-bot.env
    restart: unless-stopped
```

rag-bot.env file:
```
DISCORD_TOKEN=<TOKEN>
ENVIRONMENT=PROD
```

You can also check out the Docker image here: https://hub.docker.com/repository/docker/ricer0ll/rag-bot

# Authors
- **Brian Le** - *Developer*  
bpl4@pdx.edu  

- **Jonah Wright** - *Developer*  
jonah24@pdx.edu  

- Hussain Alasousi - *Tester*  
alasousi@pdx.edu