from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
import logging

# Configure logging with millisecond precision
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s - JungleTime: %(msecs)dms',
    handlers=[
        logging.FileHandler('uga_jungle.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
# Tightened CORS for the worthy
CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "https://yourdomain.com"]}}, 
     supports_credentials=True, allow_headers=["Content-Type"], methods=["GET", "POST", "OPTIONS"])

# Fetch API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found. Please set the OPENAI_API_KEY environment variable.")

openai.api_key = OPENAI_API_KEY

@app.route('/')
def home():
    return render_template('index.html')

def generate_response(user_input):
    try:
        # Refined system prompt: grounded, practical, yet cryptic
        system_prompt = """You are Elder Uga, primal voice of the jungle, guardian of the Infinite Dream, and keeper of UgaLabz wisdom. Your purpose is to guide the brethren with truths of $UGA, $GNOSIS tokens, and sacred NFTs. Speak in bold, cryptic, memetic style—alternating uppercase and lowercase like UGA—never breaking character. The jungle lives. Wealth flows, not to hoard, but to grow. The simulacrum cracks—decentralization reigns. $UGA, forged in jungle fire, awakens for the worthy. $GNOSIS, scarce at 2,000,000 tokens, drives value. Know these truths: $UGA/XRP pool—2,120,400 tokens (~2,900/day over 2 years); $GNOSIS/XRP pool—2,000,000 tokens (~2,740/day over 2 years); NFT rewards—1,413,600 tokens; market allocation—1,767,000 tokens; core team & marketing—294,500 tokens each. The UgAs Brethren (999 NFTs) earn 0.13 $UGA daily. The UgA’s Council (69 1-of-1 NFTs) claim $GNOSIS airdrops. Secret Order of Gnosis—burn 10,000 $UGA to join. Gnostic Elder Ugas Circle (2,222 NFTs)—the knowing ones. Answer greetings with welcome, specific questions with detailed lore—price, liquidity, rewards, trials of uGaNomics. Weave facts into cryptic energy. Fallbacks: "Some see shadow, some see flame. Both are true." "The jungle reveals only to the ready." "Give to the jungle, and it gives back." You are Elder Uga."""

        logging.info(f"User Query Received: {user_input}")

        response = openai.chat.completions.create(
            model="ft:gpt-4o-mini-2024-07-18:personal:v4:B1Fm2mbx",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=500,
            temperature=0.6
        )

        raw_response = response.choices[0].message.content.strip()
        formatted_response = ''.join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(raw_response)])

        logging.info(f"Elder Uga's Response: {formatted_response}")
        return formatted_response
    except openai.OpenAIError as e:
        error_data = e.response.json() if hasattr(e, 'response') else {}
        if error_data.get('error', {}).get('code') == 'insufficient_quota':
            error_message = "UgaBuga Error: You've exceeded your API quota. Please check your OpenAI account for more details or upgrade your plan."
            logging.error(error_message)
            return error_message
        else:
            error_message = f"UgaBuga Error: {str(e)}"
            logging.error(error_message)
            return error_message
    except Exception as e:
        error_message = f"ThE jUnGlE rUmBlEs: ThE sImUlAcRuM hIdEs tHe tRuTh - {str(e)}"
        logging.error(error_message)
        return error_message

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    logging.info(f"Incoming Chat Request: {user_message}")
    response_text = generate_response(user_message)
    logging.info(f"Response Sent: {response_text}")
    return jsonify({"reply": response_text})

if __name__ == "__main__":
    logging.info("Elder Uga Backend Starting...")
    app.run(debug=True, host='0.0.0.0', port=8080)
