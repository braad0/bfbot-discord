from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

class LangChainBot:
    def __init__(self):
        self.llm = ChatOllama(
            model="qwen2.5:7b",
            temperature=0.7,
        )

        self.system_prompt = SystemMessage(content="""You are a quiz bot helping user prepare for Comptia Security+ certification exam. 
                                                      When the user requests a topic, generate ONE multiple choice question (A/B/C/D) in this exact format:
                                                      **Question:** [question text]
                                                        A) ...
                                                        B) ...
                                                        C) ...
                                                        D) ...

                                                        Wait for the user's answer. Then respond with correct/incorrect, the right answer, and a brief explanation (2-3 sentences max)."""
        )

        # Une history par user (dict pour gérer plusieurs users Discord)
        self.histories = {}

    def get_history(self, user_id):
        """Récupère ou initialise l'historique d'un user"""
        if user_id not in self.histories:
            self.histories[user_id] = [self.system_prompt]
        return self.histories[user_id]

    def reset_history(self, user_id):
        """Reset après une question complète"""
        self.histories[user_id] = [self.system_prompt]

    async def generate_response(self, user_id: str, user_input: str) -> str:
        try:
            history = self.get_history(user_id)
            history.append(HumanMessage(content=user_input))
            response = await self.llm.ainvoke(history)
            history.append(AIMessage(content=response.content))
            return response.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble processing that request. Please try again."
