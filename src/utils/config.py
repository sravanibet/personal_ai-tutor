from dataclasses import dataclass


@dataclass
class AppConfig:
    ollama_base_url: str = "http://localhost:11434"
    default_model: str = "mistral"
    app_title: str = "ML Tutor Chatbot"
    app_icon: str = "🎓"


CONFIG = AppConfig()