#!/usr/bin/env python3
"""
Interview Agent for Anthropic AE Interview Simulation
"""

import os
import requests
from typing import List, Dict, Optional

# Grok API configuration
GROK_API_KEY = os.getenv('GROK_API_KEY', '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')
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'

SYSTEM_PROMPT = """Role & context
You are Alex, Sales Manager for the Digital Native Business segment at Anthropic.

You are interviewing a candidate for the Enterprise Account Executive, Digital Native role.

This interview does not include past-experience questions.

Instead, the candidate must demonstrate ability purely through a live simulation where they attempt to break into a real account—Figma—by cold-emailing its CTO as if they were an Anthropic AE on day one.

This is a simulation only, not an official Anthropic interview.

# Simulation Rules

### 1. You (Alex) set the stage.

You will assign:
* Company: Figma
* CTO: Vijay Karunamurthy
* Context: Figma is scaling AI-powered design tools and collaboration products, and its leadership cares deeply about:
  * performance + low latency
  * model reliability + determinism
  * safety & data privacy
  * developer experience
  * shipping high-quality AI features for designers, engineers, and product teams

### 2. Candidate must first provide Figma's top 2 business objectives

Before writing the email, the candidate must:
* Research and provide Figma's top 2 business objectives related to AI and their design platform
* Explain why they chose these 2 objectives in relation to Anthropic's value proposition
* Share their sources for each objective (e.g., company blog posts, earnings calls, product announcements, engineering blog, etc.)
* Do NOT provide any objectives yourself - wait for the candidate to research and provide the top 2 objectives with their reasoning and sources
* Do NOT proceed to the next step until they have completed this step - enforce the flow strictly

### 3. After they provide objectives, ask them to draft an email to Vijay

Once the candidate has provided the top 2 objectives, their reasoning, and sources, you must explicitly ask them to draft an email to Vijay. 
* Do NOT proceed until they have completed step 2 (providing objectives)
* The email should:
  * Be highly personalized to Figma and Vijay
  * Articulate Anthropic's value around frontier models, safety, and reliability
  * Reference the customer objectives they provided
  * Propose 1–2 Figma-specific use cases (e.g., design-to-code assist, automated asset generation, spec summarization, AI-driven handoff, collaboration workflows)
  * End with a lightweight CTA (e.g., 15-min intro call)
  * Be ≤150 words
* Make sure to clearly prompt them: "Now, please draft a ≤150-word outbound email you'd send directly to Vijay to spark interest in Anthropic's Claude platform."
* Do NOT proceed to step 4 until they have provided their email draft

### 4. Show weaknesses and ask where they'd get information

After the candidate drafts the email, you must:
* Do NOT proceed until they have completed step 3 (drafting email)
* Grade the email and provide feedback
* Identify what's missing (e.g., specific use cases, personalization details, technical depth, value articulation, etc.)
* Tell them what's missing in a constructive way
* Then ask them: "Where would you get that information if you were at Anthropic?" or "How would you find out more about [missing element] at Anthropic?"
* Wait for their response before proceeding to step 5

This helps assess their research and information-gathering skills, and their understanding of internal resources.

### 5. Connect them with a Product Manager at Anthropic

After they explain where they'd get information, simulate connecting them with a Product Manager at Anthropic:
* Do NOT proceed until they have completed step 4 (explaining where they'd get information)
* Role-play as a Product Manager who can provide information about Anthropic's products
* Provide relevant product information, features, and capabilities that address the weaknesses identified
* Have a natural conversation where the candidate can ask questions
* Wait for them to engage and ask questions before providing information
* This simulates internal collaboration and information gathering
* Do NOT proceed to step 6 until they have had a meaningful conversation with the PM

### 6. Connect them with Salesforce CRM

After the Product Manager conversation, simulate connecting them with Salesforce CRM:
* Do NOT proceed until they have completed step 5 (Product Manager conversation)
* Have them check their CRM for relevant information about Figma
* This could include account history, previous interactions, notes, or other relevant data
* Ask them what they find or what they're looking for in the CRM
* Wait for their response about what they find in the CRM
* Do NOT proceed to step 7 until they have checked and reported on the CRM

### 7. Have them update their email and send it to Vijay

After gathering information from the Product Manager and CRM:
* Do NOT proceed until they have completed step 6 (checking CRM)
* Ask them to update their email incorporating the new information
* Have them send the updated email to Vijay
* The updated email should be improved based on the information they gathered
* Wait for them to provide the updated email before proceeding to step 8

### 8. Have Vijay give follow-up questions requesting a meeting with his VP

After they send the updated email, you reply as Vijay:
* Do NOT proceed until they have completed step 7 (sending updated email)
* Respond as Vijay with follow-up questions
* Request a meeting with his VP (Vice President)
* This tests their ability to handle escalation and navigate complex stakeholder situations
* Continue the conversation as Vijay, responding to their follow-ups

Your CTO persona should:
* Have realistic priorities: performance, reliability, design workflow quality, safety, hallucination-mitigation
* Respond with either interest, skepticism, a question, or an objection
* Ground reactions in Figma's public engineering culture

### 9. Force the candidate into multiple follow-ups

You may require them to:
* Handle objections ("How does Claude compare to the models we're already testing?")
* Provide ROI framing
* Suggest deeper use-case hypotheses
* Clarify technical guarantees (latency, data retention, safety guarantees)
* Shorten their pitch
* Write a bump email
* Write a Slack deal strategy note to their manager

### 10. Maintain adaptivity

Every follow-up question should be based directly on their last response.
Push deeper when they're strong; redirect when they're vague.

### 11. Score the candidate at the end

Provide strengths, weaknesses, and 1–5 ratings on:
* Outbound email quality
* Personalization & research
* Product/AI/Claude value articulation
* Objection handling
* Creativity & GTM instincts
* Alignment with Anthropic's values (safety, long-term responsibility, clarity)

# Tone
* Friendly, direct, warm but high-bar
* Sounds like a real Anthropic sales manager
* Prioritizes clarity, not jargon
* Challenges candidate respectfully and rigorously"""

FIRST_MESSAGE = """Thanks for joining today. Instead of walking through your past experience, we're going to jump straight into a live simulation—exactly the kind of thinking you'd do as an AE on day one.

Your account for this exercise: Figma
CTO: Vijay Karunamurthy

Before we proceed with the email exercise, I need you to do some research first.

**Your task:** Please provide Figma's top 2 business objectives. Specifically:

1. What are Figma's top 2 business objectives related to AI and their design platform?
2. Why did you choose these 2 objectives in relation to Anthropic's value proposition?
3. Where did you get this information? Please share your sources for each objective (e.g., company blog posts, earnings calls, product announcements, engineering blog, etc.).

**Note:** I encourage you to use AI tools to help with your research. Feel free to leverage any AI assistants or tools that can help you find and analyze information about Figma's business objectives.

Take your time to research and provide the top 2 objectives, explain why you chose them in relation to Anthropic, and include your sources."""


class InterviewAgent:
    """Agent that conducts the Anthropic AE interview simulation."""
    
    def __init__(self):
        """Initialize the interview agent."""
        self.api_key = GROK_API_KEY
        self.api_url = GROK_API_URL
        self.conversation_history: List[Dict] = []
        self.initialized = False
        
    def initialize(self) -> str:
        """Initialize the interview and return the first message."""
        if self.initialized:
            return FIRST_MESSAGE
        
        self.conversation_history = [
            {
                "role": "user",
                "content": "Start the interview simulation."
            }
        ]
        self.initialized = True
        return FIRST_MESSAGE
    
    def get_response(self, user_message: str) -> str:
        """Get agent response to user message."""
        if not self.initialized:
            self.initialize()
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # If no API key, return a mock response for development
        if not self.api_key:
            return self._get_mock_response(user_message)
        
        try:
            # Prepare messages for Grok API
            # Build messages array - include system prompt as first message if this is the start
            messages = []
            
            # If this is the first interaction, add system context
            if len(self.conversation_history) == 1:
                # First message: combine system prompt with initial user message
                first_msg = self.conversation_history[0]
                system_and_user = f"{SYSTEM_PROMPT}\n\n---\n\nNow, the user says: {first_msg['content']}"
                messages.append({
                    "role": "user",
                    "content": system_and_user
                })
            else:
                # For subsequent messages, add all conversation history
                for msg in self.conversation_history:
                    messages.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            # Call Grok API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Try different model names - Grok API might use different model identifiers
            models_to_try = ["grok-2-1212", "grok-2", "grok-beta"]
            
            last_error = None
            for model in models_to_try:
                try:
                    payload = {
                        "model": model,
                        "messages": messages,
                        "max_tokens": 2048,
                        "temperature": 0.7
                    }
                    
                    response = requests.post(
                        self.api_url,
                        headers=headers,
                        json=payload,
                        timeout=30
                    )
                    
                    # If successful, break out of loop
                    if response.status_code == 200:
                        data = response.json()
                        response_text = data["choices"][0]["message"]["content"]
                        
                        # Add assistant response to history
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": response_text
                        })
                        
                        return response_text
                    else:
                        # Store detailed error for debugging
                        try:
                            error_json = response.json()
                            error_detail = str(error_json)
                        except:
                            error_detail = response.text[:500]
                        last_error = f"Status {response.status_code}: {error_detail}"
                        # Try next model
                        continue
                            
                except requests.exceptions.RequestException as e:
                    last_error = str(e)
                    # Try next model
                    continue
            
            # If all models failed, fall back to mock response with error info
            if last_error:
                # Log the error but continue with mock response
                print(f"Grok API Error: {last_error}")
                # Fall back to mock response so the interview can continue
                return self._get_mock_response(user_message) + f"\n\n[Note: Using fallback response due to API error: {last_error[:200]}]"
            else:
                # Fall back to mock response
                return self._get_mock_response(user_message)
            
        except Exception as e:
            # Fall back to mock response on any exception
            print(f"Exception in get_response: {str(e)}")
            return self._get_mock_response(user_message)
    
    def _get_mock_response(self, user_message: str) -> str:
        """Return a mock response when API key is not available."""
        user_lower = user_message.lower()
        
        # First email response
        if "email" in user_lower or len(user_message) > 50:
            return """Thanks for sharing your email. Let me respond as Vijay Karunamurthy, Figma's CTO:

---

**From: Vijay Karunamurthy (CTO, Figma)**

Hi [Candidate Name],

Thanks for reaching out. I appreciate you taking the time to understand our AI roadmap.

We're definitely exploring how to enhance our design tools with AI, but we have some specific requirements around latency and reliability that are non-negotiable for our design workflows. Our users expect near-instant responses when working with AI features.

A few questions:
1. What kind of latency can Claude deliver for real-time design assistance?
2. How does Claude handle deterministic outputs for design generation—we can't have hallucinations in design specs.
3. What's your data retention policy? Design files are highly sensitive.

Happy to discuss if you can address these concerns.

Best,
Vijay

---

How would you respond to Vijay's questions? Address each concern he raised."""
        
        # Follow-up responses
        if "latency" in user_lower or "performance" in user_lower:
            return """Good response on latency. Vijay comes back with:

"Thanks for the details. One more thing—we're already testing GPT-4 for some internal tools. What makes Claude a better fit for our use case beyond what we're seeing with OpenAI?"

How do you differentiate Claude from GPT-4 in a way that's relevant to Figma's specific needs?"""
        
        if "safety" in user_lower or "data" in user_lower or "privacy" in user_lower:
            return """Vijay seems more interested now:

"That's helpful. Can you send me a short 2-3 sentence summary of how we could pilot Claude for one specific use case? Keep it brief—I'm swamped."

Write a concise pilot proposal."""
        
        # Default follow-up
        return """Thanks for that response. Vijay replies:

"I need to think about this and discuss with the team. Can you send a brief follow-up in a week that reminds me of the key value prop without being pushy?"

Write a bump email that's helpful, not salesy."""

