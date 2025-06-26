# Terminal Chatbot for ComfyUI

This document outlines a simple text-based chatbot that answers questions about workflows and installation steps.

## Setup
1. Ensure Python 3.8+ is installed.
2. Run `python scripts/chatbot_tui.py` in your terminal.

The chatbot loads a small knowledge base from `knowledge_base/links.txt` and replies with helpful links or short explanations.

## Future Improvements
- Integrate a local language model (e.g., Goose or OLLama) to provide richer answers.
- Expand the knowledge base with curated tutorials and community workflows.
- Add a GUI front-end for easier interaction.
