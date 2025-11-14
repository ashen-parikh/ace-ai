# Ace AI

Current interview techniques are a bad predictor of on-job performance. Ace eliminates interviewer bias and mismatch by simulating your company for you.

## About

Ace AI is an interview simulation platform that helps companies assess candidates through realistic, job-relevant scenarios. The platform simulates real-world situations candidates would face on the job, providing a more accurate assessment of their capabilities.

## Project Structure

```
ace_ai_demo/
├── README.md
├── requirements.txt
├── anthropic_design_system.json
├── src/
│   ├── main.py
│   └── agent.py
├── templates/
│   ├── index.html
│   ├── welcome.html
│   └── interview.html
└── static/
    └── style.css
```

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
# Create .env file with your Grok API key
GROK_API_KEY=your_api_key_here
```

## Usage

Run the application:
```bash
python3 src/main.py
```

The application will start on `http://localhost:8080`

## Features

- Interactive interview simulation
- Real-time chat interface
- Step-by-step assessment flow
- Anthropic design system integration

## License

MIT
