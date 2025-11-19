'''
This module contains classes and methods for interacting with the koboldcpp server.
'''
import chromadb.utils
import requests
from src.utils.prompts.helper import system_prompt
import chromadb




class KoboldClient:
    """
    The class that handles kobold-related tasks
    """
    def __init__(self):
        self.base_url = "http://brian-le-llm.duckdns.org:5500"
        self.max_length = 150
        self.temperature = 0.6
        self.stop_sequence = ["\n", "</s>[INST]", "[/INST]"]
        self.api_key = "llmgroup9"
        self.dry_allowed_length = 2 
        self.dry_multiplier = 0.8
        self.dry_base = 1.75

        self.chat_logs: list[str] = []
        self.chat_logs.append(self.return_history())

        self.client = chromadb.EphemeralClient()
        self.collection = self.client.get_or_create_collection(
            name="glados_memory",
            configuration= {
                "hnsw": {
                    "space": "cosine"
                }
            }
        )


    def generate_prompt(self, context: str = "") -> str:
        """
        Generates a complete prompt for the kobold prompt body.

        Returns:
            str: The prompt as a string.
        """
        prompt = f"{system_prompt}\n\n"

        prompt += f"[Chat logs:]\n"

        for message in self.chat_logs:
            prompt += message + "\n"
        
        if context:
            prompt += f"[Note:] {context}\n"
        
        # Now we have the LLM generate text for GlaDOS
        prompt += "Glados:"

        return prompt


    def generate_request_body(self, prompt: str) -> dict:
        """
        Generates request body for post requesting to kobold's generation endpoint.

        Args:
            prompt (str): The prompt to be given as input to the LLM.
        Returns:
            dict: The json body as a dict.
        """

        body = {
            "max_length": self.max_length,
            "temperature": self.temperature,
            "stop_sequence": self.stop_sequence,
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
        
        rag_results = self.collection.query(query_texts=[user_msg], n_results=1)
        if rag_results:
            retrieved_context = rag_results['documents'][0][0]
        prompt = self.generate_prompt(retrieved_context)
        body = self.generate_request_body(prompt)


        try:
            result = requests.post(url=url, headers=headers, json=body)
        except Exception as e:
            raise Exception("Error communicating with Kobold server. Are you connected and is the server running?")

        response: str = result.json()["results"][0]["text"]
        response = response.strip()

        # add glados's message to the history as well.
        self.chat_logs.append(f"Glados: {response}")
        return response
    

    def clear_memory(self):
        """Clears the chat log history"""
        self.chat_logs.clear()
        self.clear_history()

    def write_to_history(self, role: str, message: str) -> None:
        """Writes a message to the conversation history file."""
        with open("/app/data/conversation_history.txt", "a", encoding="utf-8") as f:
            f.write(f"{role}: {message}\n")

    def return_history(self) -> str:
        """Returns the conversation history as a string."""
        try:
            with open("/app/data/conversation_history.txt", "r", encoding="utf-8") as f:
                history = f.read()
                return history
        except FileNotFoundError:
            return ""
        
    def clear_history(self) -> None:
        """Clears the conversation history file."""
        with open("/app/data/conversation_history.txt", "w", encoding="utf-8") as f:
            f.write("")


