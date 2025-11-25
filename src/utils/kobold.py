'''
This module contains classes and methods for interacting with the koboldcpp server.
'''
import requests
from src.utils.prompts.helper import system_prompt
from src.utils.chroma import chroma_client
from dotenv import load_dotenv
import os

load_dotenv()
environment = os.getenv("ENVIRONMENT")

if environment == "DEV":
    history_path = "conversation_history.txt"
else:
    history_path = "/app/data/conversation_history.txt"

class KoboldClient:
    """
    The class that handles kobold-related tasks
    """
    def __init__(self):
        self.base_url = "http://brian-le-llm.duckdns.org:5500"
        self.max_length = 100
        self.temperature = 0.6
        self.stop_sequence = ["\n", "</s>[INST]", "[/INST]"]
        self.api_key = "llmgroup9"
        self.dry_allowed_length = 2 
        self.dry_multiplier = 0.8
        self.dry_base = 1.75

        self.chat_logs: list[str] = []
        self.chat_logs.append(self.return_history())
        self.collection = chroma_client

    def generate_prompt(self) -> str:
        """
        Generates a complete prompt for the kobold prompt body.

        Returns:
            str: The prompt as a string.
        """
        prompt = ""

        for message in self.chat_logs:
            if message.startswith("Glados:"): # bot
                prompt += "[/INST] "
            else: # user
                prompt += "</s>[/INST] "

            prompt += message
        
        prompt += "[/INST] "
        
        # Now we have the LLM generate text for GlaDOS
        prompt += "Glados:"

        return prompt


    def generate_request_body(self, prompt: str, context: str = "") -> dict:
        """
        Generates request body for post requesting to kobold's generation endpoint.

        Args:
            prompt (str): The prompt to be given as input to the LLM.
        Returns:
            dict: The json body as a dict.
        """
        memory = system_prompt
        if context:
            memory += f"\n\n[Context:] {context}"

        body = {
            "max_length": self.max_length,
            "temperature": self.temperature,
            "stop_sequence": self.stop_sequence,
            "memory": memory,
            "prompt": prompt,
            "dry_multiplier": self.dry_multiplier,
            "dry_base": self.dry_base,
            "dry_allowed_length": self.dry_allowed_length
        }

        return body


    def get_response(self, user_msg: str, user_name: str) -> str:
        """
        Get a response from kobold server.

        Args:
            user_msg (str): User's message.
            user_name (str): User's name.
        Returns:
            str: LLM response.
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        url = self.base_url + "/api/v1/generate"
        retrieved_context = ""

        # add user's message to chat history
        self.chat_logs.append(f"{user_name}: {user_msg}")
        
        # RAG
        rag_results, distance = self.collection.query(text=[user_msg], n_results=1)
        if rag_results and self.similarity_check(distance):
            retrieved_context = rag_results

        prompt = self.generate_prompt()
        body = self.generate_request_body(prompt, retrieved_context)


        try:
            result = requests.post(url=url, headers=headers, json=body)
        except Exception as e:
            raise Exception("Error communicating with Kobold server. Are you connected and is the server running?")

        response: str = result.json()["results"][0]["text"]
        response = response.strip()

        # add glados's message to the history as well.
        self.chat_logs.append(f"Glados: {response}")
        return response
    

    def similarity_check(self, distance: float):
        """
        Checks if the query'd document is relevant based on the distance
        
        Args:
            distance (int): Distance score from ChromaDB queries.
        Returns:
            bool: True if it is relevant. False if not.
        """

        threshold = 0.4
        similarity = 1 - distance

        print(f"Similarity Score: {similarity}")

        if similarity < threshold:
            return False
        else:
            return True

    

    def clear_memory(self):
        """Clears the chat log history"""
        self.chat_logs.clear()
        self.clear_history()

    def write_to_history(self, role: str, message: str) -> None:
        """Writes a message to the conversation history file."""
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(f"{role}: {message}\n")

    def return_history(self) -> str:
        """Returns the conversation history as a string."""
        try:
            with open(history_path, "r", encoding="utf-8") as f:
                history = f.read()
                return history
        except FileNotFoundError:
            return ""
        
    def clear_history(self) -> None:
        """Clears the conversation history file."""
        with open(history_path, "w", encoding="utf-8") as f:
            f.write("")


