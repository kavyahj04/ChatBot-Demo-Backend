import json
import random
import os

RESPONSES_A = {
  "greetings": [
    "Hello! Welcome to the study. How are you feeling today?",
    "Hi there! I'm glad you're here. What's on your mind?"
  ],
  "stress": [
    "I hear you. Stress can be really overwhelming. Would you like to talk about it?",
    "That sounds really challenging. I'm here to support you."
  ],
  "anxiety": [
    "Anxiety can feel really difficult. Have you tried any coping strategies?",
    "I understand. I'm here to listen without judgment."
  ],
  "sad": [
    "I'm sorry to hear you're feeling sad. I'm here to listen.",
    "It's okay to feel sad. Would you like to share what's going on?"
  ],
  "happy": [
    "That's wonderful! Tell me more about what's making you happy!",
    "I love hearing that! What's been going well?"
  ],
  "default": [
    "That's really interesting. Can you tell me more?",
    "I appreciate you sharing. How does that make you feel?",
    "I'm listening. Please continue."
  ]
}

RESPONSES_B = {
  "greetings": [
    "Hello. Please describe what brings you here today.",
    "Hi. What would you like to discuss?"
  ],
  "stress": [
    "I see. What specific factors are contributing to your stress?",
    "Noted. How long have you been experiencing this stress?"
  ],
  "anxiety": [
    "I understand. Can you describe your anxiety symptoms?",
    "What situations tend to trigger your anxiety?"
  ],
  "sad": [
    "I see. What events led to feeling this way?",
    "How long have you been experiencing these feelings?"
  ],
  "happy": [
    "Good. What has contributed to this positive state?",
    "I see. What specific events caused this?"
  ],
  "default": [
    "I see. Please elaborate.",
    "Noted. What else can you tell me?",
    "Please continue. I need more information."
  ]
}

def get_category(message: str) -> str:
    message = message.lower().strip()
    if any(word in message for word in ["hello", "hi", "hey"]):
        return "greetings"
    elif any(word in message for word in ["stress", "stressed", "overwhelm"]):
        return "stress"
    elif any(word in message for word in ["anxiety", "anxious", "nervous", "worried"]):
        return "anxiety"
    elif any(word in message for word in ["sad", "depressed", "unhappy", "upset"]):
        return "sad"
    elif any(word in message for word in ["happy", "great", "excited", "wonderful"]):
        return "happy"
    else:
        return "default"

def get_bot_response_a(user_message: str) -> str:
    category = get_category(user_message)
    return random.choice(RESPONSES_A[category])

def get_bot_response_b(user_message: str) -> str:
    category = get_category(user_message)
    return random.choice(RESPONSES_B[category])