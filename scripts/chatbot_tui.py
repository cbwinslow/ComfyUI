#!/usr/bin/env python3
"""Simple terminal chatbot for ComfyUI knowledge base."""

import sys

KB_FILE = "knowledge_base/links.txt"

try:
    with open(KB_FILE, "r", encoding="utf-8") as f:
        KNOWLEDGE = f.read().splitlines()
except FileNotFoundError:
    KNOWLEDGE = []

HELP = "Type a question or 'quit' to exit."

print("ComfyUI Chatbot")
print(HELP)

for line in sys.stdin:
    query = line.strip().lower()
    if query in {"quit", "exit"}:
        print("Goodbye!")
        break
    if not query:
        continue
    responded = False
    for item in KNOWLEDGE:
        if query in item.lower():
            print(item)
            responded = True
    if not responded:
        print("I don't have an answer. Check the documentation in docs/.")
    print(HELP)
