from transformers import pipeline
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")

candidate_labels = [
# Is it related to Artificial Intelligence ?
"artificial intelligence",
# Is it related to politics of AI, economy of AI, or society of AI, technology of AI, science of AI, health of AI, education of AI, environment of AI, entertainment of AI, sports of AI, business of AI?
"politics", # Political implications of AI, such as regulation, governance, and international relations
"society", # Social implications of AI, such as privacy, bias, and ethical concerns
"economy", # Economic implications of AI, such as job displacement, economic growth, and wealth distribution
"technology", # Technological advancements and innovations in AI, such as new algorithms, architectures, and applications
"science", # Scientific research and advancements in AI, such as new algorithms, architectures, and breakthroughs
"health", # Health applications of AI, such as medical diagnosis and drug discovery
"education", # Educational applications of AI, such as personalized learning and intelligent tutoring systems
"environment" # Environmental effects of AI, such as energy consumption and carbon footprint
]

def classify_text(text, candidate_labels):
    result = classifier(text, candidate_labels)
    return result