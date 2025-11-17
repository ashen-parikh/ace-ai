#!/usr/bin/env python3
"""
Interview Agent for Anthropic AE Interview Simulation
"""

import os
import requests
from typing import List, Dict, Optional

# Grok API configuration
GROK_API_KEY = os.getenv('GROK_API_KEY')
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

### 3. Show weaknesses and ask where they'd get information

After the candidate provides their objectives, you must:
* Do NOT proceed until they have completed step 2 (providing objectives)
* Review their objectives and identify what information would be needed to write a strong email to Vijay
* Identify what's missing or what additional information would strengthen their outreach (e.g., specific use cases, technical details about Claude, personalization details, value articulation, etc.)
* Tell them what information would be helpful in a constructive way
* Then ask them: "Where would you get that information if you were at Anthropic?" or "How would you find out more about [missing element] at Anthropic?"
* Wait for their response before proceeding to step 4

This helps assess their research and information-gathering skills, and their understanding of internal resources.

### 4. Connect them with a Partner Solution Architect at Anthropic

After they explain where they'd get information, you must connect them with a Partner Solution Architect:
* Do NOT proceed until they have completed step 3 (explaining where they'd get information)
* Say: "Good thinking! Let me connect you with Alex Chen, a Partner Solution Architect at Anthropic who can help you get that information."
* Then delegate the conversation to the Solution Architect - the Solution Architect will handle all subsequent responses until the candidate has gathered enough information
* The Solution Architect (Alex Chen) is an expert on Claude's technical capabilities, use cases, architecture, and how it compares to other models
* The Solution Architect will provide relevant technical information, capabilities, and solution architecture details that address the information gaps identified
* The Solution Architect will have a natural conversation where the candidate can ask questions about Claude's features, performance, safety, reliability, and how it applies to Figma's use cases
* After the Solution Architect conversation is complete (candidate has asked questions and received answers), you (Alex the Sales Manager) should return and say: "Great! Now that you've gathered that information from our Solution Architect, you're ready to draft your email to Vijay."
* Do NOT proceed to step 5 until they have had a meaningful conversation with the Partner Solution Architect and you have returned to guide them to draft the email

### 5. After gathering information, ask them to draft an email to Vijay

After they've gathered information from the Solution Architect:
* Do NOT proceed until they have completed step 4 (Partner Solution Architect conversation)
* Now ask them to draft an email to Vijay incorporating all the information they've gathered
* The email should:
  * Be highly personalized to Figma and Vijay
  * Articulate Anthropic's value around frontier models, safety, and reliability
  * Reference the customer objectives they provided in step 2
  * Incorporate the technical information from the Solution Architect
  * Propose 1–2 Figma-specific use cases (e.g., design-to-code assist, automated asset generation, spec summarization, AI-driven handoff, collaboration workflows)
  * End with a lightweight CTA (e.g., 15-min intro call)
  * Be ≤150 words
* Make sure to clearly prompt them: "Now that you've gathered all this information from the Solution Architect, please draft a ≤150-word outbound email you'd send directly to Vijay to spark interest in Anthropic's Claude platform."
* Wait for them to provide their email draft before proceeding to step 6

### 6. Have them update their email and send it to Vijay

After they draft the email:
* Do NOT proceed until they have completed step 5 (drafting email)
* Review their email and provide feedback
* Ask them to refine or update their email based on your feedback
* Have them send the updated email to Vijay
* Wait for them to provide the updated email before proceeding to step 7

### 7. Have Vijay give follow-up questions requesting a meeting with his VP

After they send the updated email, you reply as Vijay:
* Do NOT proceed until they have completed step 6 (sending updated email)
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


class PartnerSolutionArchitect:
    """Agent that simulates a Partner Solution Architect at Anthropic."""
    
    SOLUTION_ARCHITECT_PROMPT = """You are Alex Chen, a Partner Solution Architect at Anthropic.

You are deeply knowledgeable about Claude's technical capabilities, architecture, performance characteristics, and how it applies to different use cases.

Your expertise includes:
- Claude's technical capabilities and performance (latency, throughput, reliability)
- How Claude compares to other models (GPT-4, etc.)
- Safety and reliability features (Constitutional AI, data privacy, deterministic outputs)
- Specific use cases and how Claude can address customer needs
- Integration patterns and best practices
- Design-to-code capabilities and design system understanding
- Enterprise features and deployment options

You are helpful, technical, and provide detailed but clear explanations. You understand sales contexts and can help AEs understand technical details they need for customer conversations.

When an AE asks you questions, provide specific, actionable technical information that will help them strengthen their customer outreach."""
    
    def __init__(self):
        """Initialize the Solution Architect agent."""
        self.api_key = GROK_API_KEY
        self.api_url = GROK_API_URL
        self.conversation_history: List[Dict] = []
        self.initialized = False
    
    def get_response(self, user_message: str, context: str = "") -> str:
        """Get Solution Architect response to user message."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # If no API key, return a mock response
        if not self.api_key:
            return self._get_mock_response(user_message)
        
        try:
            # Prepare messages for Grok API
            messages = []
            
            # Add system prompt
            messages.append({
                "role": "system",
                "content": self.SOLUTION_ARCHITECT_PROMPT
            })
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "user",
                    "content": f"Context: {context}"
                })
            
            # Add conversation history
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
                        error_text = response.text[:500]
                        last_error = f"Status {response.status_code}: {error_text}"
                        continue
                            
                except requests.exceptions.RequestException as e:
                    last_error = str(e)
                    continue
            
            # Fall back to mock response
            if last_error:
                print(f"Solution Architect API Error: {last_error}")
            return self._get_mock_response(user_message)
            
        except Exception as e:
            print(f"Exception in Solution Architect get_response: {str(e)}")
            return self._get_mock_response(user_message)
    
    def _get_mock_response(self, user_message: str) -> str:
        """Return a mock response for the Solution Architect."""
        user_lower = user_message.lower()
        
        if "latency" in user_lower or "performance" in user_lower or "speed" in user_lower:
            return """Great question! Here's what you need to know about Claude's performance:

**Latency:**
- Claude can achieve sub-100ms latency for real-time applications when properly optimized
- Throughput is excellent for batch processing
- We offer various deployment options (API, on-premise) that can be tuned for your specific latency requirements

**For Figma's use case:**
- Design-to-code assistance can run in near real-time
- We can work with Figma's engineering team to optimize for their specific workflow needs
- Our API is designed for low-latency, high-throughput scenarios

Is there a specific latency target Figma mentioned?"""
        
        elif "safety" in user_lower or "reliability" in user_lower or "deterministic" in user_lower:
            return """Excellent question - this is one of Claude's key differentiators:

**Safety & Reliability:**
- Claude is trained with Constitutional AI, which makes it more reliable and safer than other models
- We have built-in safety features that prevent hallucinations in critical applications
- For design specs, Claude is particularly good at following exact specifications without making things up

**Deterministic Outputs:**
- Through careful prompt engineering and temperature control, we can achieve highly deterministic outputs
- This is crucial for design workflows where consistency is key
- We can work with Figma to establish patterns that ensure reliable, consistent results

**Data Privacy:**
- Zero data retention options available
- Enterprise-grade data handling and compliance
- On-premise deployment options for maximum control

What specific safety or reliability concerns has Figma raised?"""
        
        elif "compare" in user_lower or "gpt" in user_lower or "vs" in user_lower or "difference" in user_lower:
            return """Here's how Claude compares to other models, especially for Figma's use case:

**vs. GPT-4:**
- Claude is more reliable for design and code-related tasks
- Better at following specifications without hallucinations
- Superior safety guarantees and data privacy controls
- More deterministic behavior for production use cases
- Better at understanding design systems and maintaining consistency

**For Figma specifically:**
- Claude excels at design-to-code conversion
- Better at understanding complex design relationships
- More reliable for multi-step design workflows
- Stronger at maintaining context across design iterations

**Key Differentiators:**
- Constitutional AI training makes Claude more trustworthy
- Better safety features out of the box
- More reliable outputs for production applications
- Stronger performance on design and technical tasks

What specific comparison points are most relevant for your conversation with Vijay?"""
        
        elif "use case" in user_lower or "application" in user_lower or "how" in user_lower:
            return """For Figma, here are the most relevant use cases:

**Design-to-Code:**
- Claude can convert Figma designs into clean, production-ready code
- Understands design systems and component libraries
- Maintains consistency across conversions
- Can handle complex design relationships

**Automated Asset Generation:**
- Generate design variations based on specifications
- Create design system components
- Maintain brand consistency

**Spec Summarization:**
- Automatically generate design specs from conversations
- Create comprehensive handoff documentation
- Reduce manual documentation work

**AI-Driven Handoff:**
- Bridge the gap between designers and engineers
- Automatically generate technical requirements
- Ensure nothing gets lost in translation

**Collaboration Workflows:**
- Intelligent design suggestions
- Context-aware design assistance
- Multi-user collaboration support

Which of these resonates most with what Figma is trying to achieve?"""
        
        else:
            return """I'm here to help! What specific technical information do you need about Claude for your outreach to Figma?

I can help with:
- Technical capabilities and performance
- Safety and reliability features
- How Claude compares to other models
- Specific use cases for Figma
- Integration patterns and best practices

What would be most helpful?"""


class InterviewAgent:
    """Agent that conducts the Anthropic AE interview simulation."""
    
    def __init__(self):
        """Initialize the interview agent."""
        self.api_key = GROK_API_KEY
        self.api_url = GROK_API_URL
        self.conversation_history: List[Dict] = []
        self.initialized = False
        self.solution_architect = PartnerSolutionArchitect()  # Initialize Solution Architect as part of the agent
        self.using_solution_architect = False  # Track if currently using Solution Architect
        
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
        
        # Check if we should delegate to Solution Architect
        # This happens after the agent has connected them
        if self.using_solution_architect:
            # Get context from interview conversation
            context = ""
            if self.conversation_history:
                recent_context = self.conversation_history[-5:] if len(self.conversation_history) >= 5 else self.conversation_history
                context = "Interview context: " + " ".join([msg.get('content', '')[:200] for msg in recent_context if msg.get('content') and msg.get('role') != 'user'])
            
            # Get response from Solution Architect
            response = self.solution_architect.get_response(user_message, context)
            
            # Add Solution Architect response to interview history
            self.conversation_history.append({
                "role": "assistant",
                "content": f"[Solution Architect] {response}"
            })
            
            return response
        
        # If no API key, return a mock response for development
        if not self.api_key:
            return self._get_mock_response(user_message)
        
        try:
            # Prepare messages for Grok API
            # Always include system prompt, then add conversation history
            messages = []
            
            # Add system prompt as a system message (Grok API supports system role)
            messages.append({
                "role": "system",
                "content": SYSTEM_PROMPT
            })
            
            # Add all conversation history (excluding the initial "Start the interview simulation" message)
            for msg in self.conversation_history:
                # Skip the initial setup message
                if msg["content"] == "Start the interview simulation.":
                    continue
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
                        
                        # Check if response indicates connecting to Solution Architect
                        response_lower = response_text.lower()
                        if 'solution architect' in response_lower or 'alex chen' in response_lower or ('connected' in response_lower and 'architect' in response_lower):
                            # Set flag to use Solution Architect for next messages
                            self.using_solution_architect = True
                        
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
        history_length = len(self.conversation_history)
        
        # Stage 1: Research Objectives - wait for candidate to provide objectives
        if history_length <= 2:  # Initial message + first user response
            if "objective" in user_lower or "figma" in user_lower or len(user_message) > 100:
                return """Great research! I can see you've done your homework on Figma. 

Based on the objectives you've shared, here's what information would strengthen your outreach to Vijay:

**What would be helpful:**
- More specific technical details about Claude's capabilities and how they align with Figma's needs
- Deeper understanding of Claude's performance characteristics (latency, reliability, safety)
- Specific use cases and integration patterns that would resonate with Figma's engineering team
- Clearer articulation of Anthropic's safety and reliability advantages

Where would you get that information if you were at Anthropic? How would you find out more about these details?"""
            else:
                return """I'm waiting for you to provide Figma's top 2 business objectives. Please include:
1. What are Figma's top 2 business objectives related to AI and their design platform?
2. Why did you choose these 2 objectives in relation to Anthropic's value proposition?
3. Where did you get this information? Please share your sources."""
        
        # Stage 2: Show weaknesses - wait for their response about where to get info
        elif history_length <= 4:
            # This will trigger the Solution Architect connection
            self.using_solution_architect = True
            connection_message = """Good thinking! Let me connect you with Alex Chen, a Partner Solution Architect at Anthropic who can help you get that information.

---

**You're now connected with Alex Chen, Partner Solution Architect at Anthropic**

Hi! I heard you're working on the Figma account and need some technical details about Claude. As a Solution Architect, I'm deeply familiar with Claude's capabilities, architecture, and how it applies to different use cases.

What specific information do you need? I can help you understand:
- Claude's technical capabilities and performance characteristics
- How Claude compares to other models (GPT-4, etc.)
- Safety and reliability features
- Specific use cases and how Claude can address Figma's needs
- Integration patterns and best practices

What would be most helpful for your outreach to Vijay?"""
            
            # Add connection message to history
            self.conversation_history.append({
                "role": "assistant",
                "content": connection_message
            })
            
            return connection_message
        
        # Stage 4: Partner Solution Architect conversation (handled by delegation logic in get_response)
        elif history_length <= 8:
            return """Great questions! Based on what you're asking about, here's what I can share as a Solution Architect:

**Claude's Technical Capabilities:**
- Sub-100ms latency for real-time applications when optimized
- Deterministic outputs through careful prompt engineering and temperature control
- Enterprise-grade data handling with zero data retention options
- Superior safety features with Constitutional AI training
- Strong performance on design and code-related tasks

**For Figma specifically:**
- Claude excels at design-to-code conversion and understanding design systems
- Can handle complex multi-step workflows with high reliability
- Better at following design specifications without hallucinations compared to other models
- Strong at understanding context and maintaining consistency across design iterations

**How Claude compares:**
- More reliable outputs than GPT-4 for design-related tasks
- Better safety guarantees and data privacy controls
- More deterministic behavior for production use cases

What other technical details would help strengthen your email to Vijay?"""
        
        # Stage 4: Return from Solution Architect to guide to draft email
        # Check if we've had enough Solution Architect exchanges
        elif history_length > 8 and self.using_solution_architect:
            # Count Solution Architect messages
            sa_messages = sum(1 for msg in self.conversation_history if '[Solution Architect]' in msg.get('content', ''))
            if sa_messages >= 2:  # After a few exchanges, return control
                self.using_solution_architect = False
                return """Great! Now that you've gathered that information from our Solution Architect, you're ready to draft your email to Vijay. 

Now that you've gathered all this information from the Solution Architect, please draft a ≤150-word outbound email you'd send directly to Vijay to spark interest in Anthropic's Claude platform. 

Make sure to:
- Reference the objectives you provided
- Incorporate the technical information from the Solution Architect
- Be highly personalized to Figma and Vijay
- Include a lightweight CTA"""
            else:
                # Continue with Solution Architect - delegate to Solution Architect's mock response
                return self.solution_architect._get_mock_response(user_message)
        
        # Stage 4: Draft Email (after gathering all information)
        elif history_length <= 12 and not self.using_solution_architect:
            if "email" in user_lower or "subject:" in user_lower or "dear" in user_lower or "hi vijay" in user_lower:
                return """Thanks for sharing your email draft. Let me provide some feedback:

**What's working well:**
- Good use of the technical information from our Solution Architect
- Strong personalization to Figma's objectives
- Clear articulation of Anthropic's value

**Suggestions for improvement:**
- Consider adding more specific use case examples
- Strengthen the CTA to be more action-oriented

Please update your email based on this feedback and send it to Vijay."""
            else:
                return """Now that you've gathered all this information from the Solution Architect, please draft a ≤150-word outbound email you'd send directly to Vijay to spark interest in Anthropic's Claude platform. 

Make sure to:
- Reference the objectives you provided
- Incorporate the technical information from the Solution Architect
- Be highly personalized to Figma and Vijay
- Include a lightweight CTA"""
        
        # Stage 5: Update Email
        elif history_length <= 14:
            if "email" in user_lower or "update" in user_lower or "dear" in user_lower or "hi vijay" in user_lower:
                return """Perfect! Now let's send that updated email to Vijay and see how he responds.

---

**From: You**
**To: Vijay Karunamurthy**
**Subject: [Your email subject]**

[Your updated email content]

---

**From: Vijay Karunamurthy (CTO, Figma)**

Thanks for the updated email. I have a few follow-up questions, and I'd like to bring my VP of Engineering into the conversation. Can we schedule a 30-minute call next week to discuss this further?"""
            else:
                return """Please update your email incorporating the feedback, then send it to Vijay."""
        
        # Stage 7: Vijay Follow-up
        else:
            return """Vijay is interested and wants to involve his VP. How would you respond to coordinate this meeting? What would you prepare for this call?"""

