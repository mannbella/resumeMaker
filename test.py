from google import genai

client = genai.Client()

print("Models available to your API key:")
for model in client.models.list():
    print(model.name)