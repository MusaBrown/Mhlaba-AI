#!/usr/bin/env python3
"""
JARVIS - Free AI Version
Uses Groq (free tier) or built-in smart responses
No API costs!
"""

import speech_recognition as sr
import pyttsx3
from datetime import datetime
import os
import sys

print("="*60)
print("JARVIS - FREE AI VERSION")
print("="*60)

# Setup speech
recognizer = sr.Recognizer()
microphone = sr.Microphone()
recognizer.energy_threshold = 3000
recognizer.dynamic_energy_threshold = False
recognizer.pause_threshold = 1.0

# User info
USER_NAME = "sir"  # Default name

# Try Groq (FREE AI alternative to OpenAI)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_GROQ = False

if GROQ_API_KEY:
    try:
        import groq
        groq_client = groq.Client(api_key=GROQ_API_KEY)
        USE_GROQ = True
        print("[✓] Connected to Groq AI (FREE)")
    except:
        print("[!] Groq not installed. Run: pip install groq")
else:
    print("[i] Using Smart Built-in Mode (No API needed)")
    print("    For even smarter AI, get FREE Groq key:")
    print("    https://console.groq.com/keys")
    print("    Then run: setx GROQ_API_KEY your-key")

# Smart knowledge base (built-in, no API cost)
KNOWLEDGE_BASE = {
    # Science
    "newton first law": "Newton's First Law states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and direction unless acted upon by an unbalanced force. This is also called the Law of Inertia.",
    "newton second law": "Newton's Second Law states that Force equals Mass times Acceleration (F=ma). The more mass an object has, the more force is needed to accelerate it.",
    "newton third law": "Newton's Third Law states that for every action, there is an equal and opposite reaction. When you push on a wall, the wall pushes back with equal force.",
    "gravity": "Gravity is a fundamental force of nature that causes objects with mass to attract each other. On Earth, it gives weight to physical objects and causes them to fall toward the ground when dropped.",
    "quantum": "Quantum mechanics is the branch of physics that studies matter and energy at the smallest scales. It describes how particles like electrons behave in strange ways - they can exist in multiple states at once and be connected across vast distances.",
    "relativity": "Einstein's Theory of Relativity includes Special Relativity (E=mc², nothing travels faster than light) and General Relativity (gravity curves spacetime). It changed our understanding of space, time, and the universe.",
    "black hole": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape from it. They form when massive stars collapse at the end of their lives.",
    
    # Tech
    "computer": "A computer is an electronic device that processes data according to instructions. Modern computers use binary (0s and 1s) and can perform billions of calculations per second.",
    "programming": "Programming is writing instructions for computers using special languages like Python, JavaScript, or C++. It's like giving the computer a recipe to follow.",
    "python": "Python is a popular, easy-to-learn programming language known for its readable syntax. It's used for web development, data science, AI, automation, and more.",
    "artificial intelligence": "Artificial Intelligence is computer systems that can perform tasks that normally require human intelligence, like understanding speech, recognizing images, making decisions, and learning from experience.",
    "machine learning": "Machine Learning is a type of AI where computers learn from data without being explicitly programmed. They find patterns and make predictions based on examples.",
    "blockchain": "Blockchain is a digital ledger that records transactions across many computers. It's decentralized, secure, and transparent. Bitcoin and other cryptocurrencies use blockchain technology.",
    "internet": "The Internet is a global network of connected computers. It uses standardized protocols (like TCP/IP) to allow devices worldwide to communicate and share information.",
    
    # General knowledge
    "cook pasta": "To cook pasta: 1) Boil water in a large pot with salt. 2) Add pasta and stir. 3) Cook for time on package (usually 8-12 minutes). 4) Test for doneness (al dente). 5) Drain and add sauce!",
    "pasta": "To cook pasta: 1) Boil water in a large pot with salt. 2) Add pasta and stir. 3) Cook for time on package (usually 8-12 minutes). 4) Test for doneness (al dente). 5) Drain and add sauce!",
    "meaning of life": "The meaning of life is one of philosophy's biggest questions! Some say it's to seek happiness, others say to help others, create, love, or find your own purpose. What do you think it is?",
    "mars": "Mars is the fourth planet from the Sun, often called the Red Planet due to iron oxide on its surface. It's a cold, desert world with the largest volcano (Olympus Mons) in the solar system. NASA and SpaceX plan to send humans there.",
    "sun": "The Sun is a star at the center of our solar system. It's about 93 million miles away, contains 99.86% of the solar system's mass, and provides the energy that powers life on Earth.",
    "dna": "DNA (Deoxyribonucleic Acid) is the molecule that carries genetic instructions for all known living organisms. It's shaped like a double helix and contains the code for building and maintaining an organism.",
    "evolution": "Evolution is the process by which species change over time through natural selection. Organisms with traits better suited to their environment tend to survive and reproduce, passing those traits to offspring.",
    
    # AI/Machine Learning
    "neural network": "Neural networks are computer systems inspired by the human brain. They consist of interconnected nodes (like neurons) organized in layers. Each connection has a weight that adjusts as the network learns. They're used for image recognition, language processing, and more.",
    "deep learning": "Deep Learning is a type of machine learning using neural networks with many layers (hence 'deep'). It powers things like facial recognition, self-driving cars, and ChatGPT. The multiple layers allow the system to learn complex patterns.",
    "neural": "Neural networks are computer systems inspired by the human brain. They consist of interconnected nodes (like neurons) organized in layers. Each connection has a weight that adjusts as the network learns. They're used for image recognition, language processing, and more.",
    
    # Chemistry
    "atom": "An atom is the smallest unit of matter that retains the properties of an element. It consists of protons and neutrons in the nucleus, with electrons orbiting around it. Everything in the universe is made of atoms.",
    "molecule": "A molecule is two or more atoms bonded together. For example, water (H2O) is a molecule made of two hydrogen atoms and one oxygen atom bonded together.",
    "periodic table": "The Periodic Table is a chart that organizes all known chemical elements by their properties. It was created by Dmitri Mendeleev in 1869. Elements are arranged by atomic number, with similar elements in columns called groups.",
    
    # Math
    "pythagorean theorem": "The Pythagorean Theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides: a² + b² = c². It's fundamental to geometry and used in construction, navigation, and physics.",
    "calculus": "Calculus is a branch of mathematics that studies continuous change. It has two main parts: differential calculus (rates of change and slopes) and integral calculus (accumulation and areas). It's essential for physics and engineering.",
    
    # History
    "world war 2": "World War II was a global conflict from 1939 to 1945. It involved most of the world's nations divided into Allies and Axis powers. It ended with the defeat of Nazi Germany and Imperial Japan, and led to the formation of the United Nations.",
    "world war ii": "World War II was a global conflict from 1939 to 1945. It involved most of the world's nations divided into Allies and Axis powers. It ended with the defeat of Nazi Germany and Imperial Japan, and led to the formation of the United Nations.",
    "ww2": "World War II was a global conflict from 1939 to 1945. It involved most of the world's nations divided into Allies and Axis powers. It ended with the defeat of Nazi Germany and Imperial Japan, and led to the formation of the United Nations.",
    "einstein": "Albert Einstein (1879-1955) was a German-born theoretical physicist who developed the theory of relativity. His famous equation E=mc² showed that mass and energy are interchangeable. He won the Nobel Prize in Physics in 1921.",
    "tesla": "Nikola Tesla (1856-1943) was an inventor and electrical engineer known for his work on alternating current (AC) electrical systems. He pioneered technologies like the Tesla coil, wireless communication, and experimented with X-rays.",
    
    # Health/Medicine
    "vitamin": "Vitamins are organic compounds that our bodies need in small amounts for proper functioning. They're essential for growth, immune function, and metabolism. There are 13 essential vitamins including A, C, D, E, K, and B vitamins.",
    "immune system": "The immune system is your body's defense against infections and diseases. It includes white blood cells, antibodies, lymph nodes, and organs like the spleen and thymus. It recognizes and destroys harmful bacteria, viruses, and other invaders.",
    
    # Geography
    "amazon rainforest": "The Amazon Rainforest is the world's largest tropical rainforest, covering much of northwestern Brazil and extending into other South American countries. It produces about 20% of the world's oxygen and contains about 10% of all species on Earth.",
    "sahara": "The Sahara Desert is the world's largest hot desert, covering most of North Africa. It's about the size of the United States and is known for its sand dunes, extreme temperatures (up to 136°F), and very little rainfall.",
    
    # More cooking
    "cook rice": "To cook rice: 1) Rinse rice until water runs clear. 2) Use 1 part rice to 2 parts water. 3) Bring to boil, then reduce heat to low. 4) Cover and simmer 15-20 minutes. 5) Let rest 5 minutes, then fluff with fork.",
    "cook egg": "To fry an egg: Heat butter or oil in a pan over medium heat. Crack egg into pan. Cook 2-3 minutes for sunny side up, or flip and cook 1 minute more for over easy. For scrambled: whisk eggs, pour into pan, stir gently until cooked.",
    "bake cake": "Basic cake: Mix 2 cups flour, 1.5 cups sugar, 3.5 tsp baking powder, 1 cup milk, 0.5 cup butter, 2 eggs, and 1 tsp vanilla. Bake at 350°F (175°C) for 30-35 minutes in greased pans. Cool before frosting.",
}

def speak(text):
    """Speak text - replaces {name} with user's name"""
    global USER_NAME
    text = text.replace("{name}", USER_NAME)
    print(f"\n🔊 JARVIS: \"{text}\"")
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 175)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except:
        pass

def listen():
    """Listen for command"""
    with microphone as source:
        print("\n[LISTENING...]")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            print("[Processing...]")
            text = recognizer.recognize_google(audio)
            print(f"[You: '{text}']")
            return text
        except:
            return None

def ask_groq(question):
    """Ask Groq AI (FREE)"""
    if not USE_GROQ:
        return None
    try:
        print("[🧠 Thinking with Groq AI...]")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Fast, free, smart
            messages=[
                {"role": "system", "content": "You are JARVIS from Iron Man. Be helpful, witty, and concise."},
                {"role": "user", "content": question}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Groq Error: {e}]")
        return None

def search_knowledge(question):
    """Search built-in knowledge"""
    question_lower = question.lower()
    
    # Direct keyword matching
    for keyword, answer in KNOWLEDGE_BASE.items():
        if keyword in question_lower:
            return answer
    
    # Partial matches
    for keyword, answer in KNOWLEDGE_BASE.items():
        words = keyword.split()
        matches = sum(1 for word in words if word in question_lower)
        if matches >= 2:  # At least 2 words match
            return answer
    
    return None

def process(command):
    """Process command"""
    cmd_lower = command.lower().strip().replace("jarvis", "").strip()
    
    if not cmd_lower:
        return True
    
    # Exit
    if cmd_lower in ['exit', 'quit', 'goodbye', 'bye']:
        speak("Shutting down. It was a pleasure assisting you, sir.")
        return False
    
    # Time/Date
    if 'time' in cmd_lower:
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")
        return True
    if 'date' in cmd_lower or 'day is it' in cmd_lower:
        speak(f"Today is {datetime.now().strftime('%A, %B %d, %Y')}")
        return True
    
    # Open apps
    if cmd_lower.startswith('open '):
        app = cmd_lower.replace('open ', '').strip()
        speak(f"Opening {app}")
        os.system(f'start {app}')
        return True
    
    # Search web
    if 'search' in cmd_lower:
        query = cmd_lower.replace('search', '').replace('for', '').strip()
        speak(f"Searching for {query}")
        import webbrowser
        webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
        return True
    
    # Try Groq AI first (FREE)
    if USE_GROQ:
        groq_answer = ask_groq(command)
        if groq_answer:
            speak(groq_answer)
            return True
    
    # Try built-in knowledge
    knowledge = search_knowledge(cmd_lower)
    if knowledge:
        speak(knowledge)
        return True
    
    # Name handling
    global USER_NAME
    
    if "my name is" in cmd_lower or "call me" in cmd_lower:
        # Extract name
        if "my name is" in cmd_lower:
            name = cmd_lower.split("my name is")[-1].strip().title()
        else:
            name = cmd_lower.split("call me")[-1].strip().title()
        
        if name:
            USER_NAME = name
            speak(f"Understood. I will address you as {USER_NAME} from now on.")
            return True
    
    if "what is my name" in cmd_lower or "do you know my name" in cmd_lower:
        if USER_NAME != "sir":
            speak(f"Your name is {USER_NAME}, of course.")
        else:
            speak("You haven't told me your name yet. Say 'my name is' followed by your name.")
        return True
    
    # Basic responses
    BASIC = {
        "hello": "Hello {name}! JARVIS at your service. I have extensive knowledge about science, technology, and more. What would you like to know?",
        "hi": "Greetings! How may I assist you today?",
        "hey": "Hello! Ready to help.",
        "how are you": "All systems functioning at peak efficiency, thank you for asking!",
        "who are you": "I am JARVIS - Just A Rather Very Intelligent System. I'm your AI assistant, {name}, with knowledge of physics, computing, cooking, and much more!",
        "what can you do": "I can explain scientific concepts like Newton's laws or quantum physics, help with cooking, discuss technology, open applications, search the web, and have intelligent conversations. Try asking me anything!",
        "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
        "thank": "You're most welcome, {name}!",
        "thanks": "My pleasure, {name}!",
    }
    
    for key, resp in BASIC.items():
        if key in cmd_lower:
            speak(resp)
            return True
    
    # Don't know
    speak("I don't have that specific information in my knowledge base yet. Try asking about physics, space, cooking, or technology! Or say 'search for' to look it up online.")
    return True

# Main
print("[Calibrating...]")
with microphone as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

print("\n" + "="*60)
if USE_GROQ:
    print("🔥 JARVIS WITH FREE GROQ AI")
else:
    print("🤖 JARVIS SMART MODE (No API costs)")
    print("   Get FREE AI key: https://console.groq.com/keys")
print("="*60)

speak("JARVIS online. I have extensive built-in knowledge about science, technology, and more. Ask me anything!")

print("\n💡 WHAT TO ASK:")
print('  Science: "Explain Newton\'s First Law" | "What is quantum physics"')
print('  Tech: "What is artificial intelligence" | "Explain blockchain"')
print('  Space: "What is a black hole" | "Tell me about Mars"')
print('  Cooking: "How to cook pasta"')
print('  Or: "Open notepad" | "What time is it" | "Exit"')
print("="*60)

while True:
    text = listen()
    if text and not process(text):
        break

print("\n[Shutdown complete]")
