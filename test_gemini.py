# test_gemini.py

import os
import google.generativeai as genai

# Configure API
api_key = os.getenv("GEMINI_API_KEY", "AIzaSyC4oa814AA4CB_gGxTyyZjqp1DYZH6656U")
genai.configure(api_key=api_key)

print("Conexão bem-sucedida. Listando modelos disponíveis que suportam 'generateContent':")
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(f"- {model.name}")

# Test content generation with a simple prompt
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content("Olá, tudo bem?")
    print("\nTeste de geração de conteúdo bem-sucedido:")
    print(response.text)
except Exception as e:
    print(f"\nErro ao gerar conteúdo: {e}")