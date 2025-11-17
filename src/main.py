#!/usr/bin/env python3
"""
Main entry point for the application.
"""

import os
import sys
import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv

# Add src directory to path
basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, basedir)

from agent import InterviewAgent

# Load environment variables
load_dotenv()

# Get the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Go up one level to the project root
project_root = os.path.dirname(basedir)

app = Flask(__name__, 
            template_folder=os.path.join(project_root, 'templates'),
            static_folder=os.path.join(project_root, 'static'))
app.secret_key = 'your-secret-key-here'  # Needed for session

# Initialize interview agent (one per session)
agents = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the welcome page as the first page."""
    return render_template('welcome.html')

@app.route('/interview', methods=['GET', 'POST'])
def interview():
    """Render the interview page after name is entered on welcome page."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            session['name'] = name
            return redirect(url_for('interview'))
    
    name = session.get('name')
    if not name:
        return redirect(url_for('index'))
    
    # Initialize agent for this session if not exists
    session_id = session.get('session_id', None)
    if not session_id:
        session_id = os.urandom(16).hex()
        session['session_id'] = session_id
    
    if session_id not in agents:
        agents[session_id] = InterviewAgent()
    
    return render_template('interview.html', name=name)

@app.route('/api/chat/init', methods=['POST'])
def init_chat():
    """Initialize the interview chat."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session'}), 400
    
    if session_id not in agents:
        agents[session_id] = InterviewAgent()
    
    agent = agents[session_id]
    first_message = agent.initialize()
    
    return jsonify({
        'message': first_message,
        'role': 'assistant'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with the interview agent."""
    session_id = session.get('session_id')
    if not session_id:
        return jsonify({'error': 'No session'}), 400
    
    if session_id not in agents:
        agents[session_id] = InterviewAgent()
        agents[session_id].initialize()
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    agent = agents[session_id]
    
    # Get response from agent - it will automatically delegate to Solution Architect if needed
    agent_response = agent.get_response(user_message)
    
    # Check if we're currently using Solution Architect to set the speaker
    speaker = None
    if agent.using_solution_architect:
        speaker = 'Alex Chen (Solution Architect)'
    
    return jsonify({
        'message': agent_response,
        'role': 'assistant',
        'speaker': speaker
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)

