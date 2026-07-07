from backend.ai.llm import llm_service

llm = llm_service.get_llm()

response = llm.invoke("Hello")

print(response.content)