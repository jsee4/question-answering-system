import google.generativeai as genai

# PASTE YOUR KEY HERE
genai.configure(api_key="AIzaSyCTiHc9QNZFUoHdxyJQJ2oF6mWlvSFhAJM") 

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")