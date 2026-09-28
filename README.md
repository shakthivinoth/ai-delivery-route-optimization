# AI-Based Multi-Stop Delivery Route Optimization and Driver Safety Support Chatbot

A beginner-friendly college project with two modules:
1. **Route Optimizer** - Nearest Neighbor algorithm + Leaflet/OpenStreetMap map
2. **Safety Chatbot** - TF-IDF + Cosine Similarity over `policy/safety_policy.txt`

## How to run on Mac (VS Code)
1. Unzip the project and open the `delivery-ai-project` folder in VS Code.
2. Open the terminal (Terminal > New Terminal) and run:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
3. Open your browser at: **http://127.0.0.1:5000**
4. Stop the server with `Ctrl + C`.

Note: internet is needed only to load the Leaflet library and map tiles.

## Project structure
- `app.py` - Flask server and API routes
- `route_optimizer.py` - sample data + Nearest Neighbor algorithm
- `chatbot.py` - TF-IDF + cosine similarity chatbot
- `policy/safety_policy.txt` - the only knowledge source for the chatbot
- `templates/index.html`, `static/style.css`, `static/script.js` - the dashboard

## Try it
- Click **Optimize Route** -> Warehouse -> Customer C -> Customer D -> Customer B -> Customer A (17 km, 34 min at 30 km/h)
- Ask: "Can I use my phone while driving?", "What to do after an accident?", "Who won the world cup?" (not in policy -> refusal message)

## Change things
- Add rules: edit `policy/safety_policy.txt` (`# Heading` line, then one rule per line) and restart.
- Change distances/coordinates: edit `route_optimizer.py`.
- Change speed: Settings page in the app (default 30 km/h).
