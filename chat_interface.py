import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ChatInterface:
    def __init__(self):
        """Initialize the chat interface with OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
            
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        self.current_session = None
        
    def start_new_conversation(self):
        """Start a new conversation session"""
        if self.current_session:
            self.save_conversation()
            
        self.current_session = {
            'start_time': datetime.now().isoformat(),
            'messages': []
        }
        self.conversation_history = []
        
    def send_message(self, message: str, system_prompt: Optional[str] = None) -> str:
        """Send a message and get response"""
        try:
            if not self.current_session:
                self.start_new_conversation()
                
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
                
            # Add conversation history
            messages.extend([{
                "role": "user" if i % 2 == 0 else "assistant",
                "content": msg
            } for i, msg in enumerate(self.conversation_history)])
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Get response from API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response text
            response_text = response.choices[0].message.content
            
            # Update history
            self.conversation_history.extend([message, response_text])
            
            # Record in current session
            self.current_session['messages'].append({
                'timestamp': datetime.now().isoformat(),
                'user_message': message,
                'assistant_message': response_text,
                'system_prompt': system_prompt
            })
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error in chat completion: {str(e)}")
            raise
            
    def save_conversation(self, filename: Optional[str] = None):
        """Save the current conversation to a file"""
        try:
            if not self.current_session:
                logger.warning("No active session to save")
                return
                
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"conversation_{timestamp}.json"
                
            # Ensure output directory exists
            os.makedirs('output', exist_ok=True)
            filepath = os.path.join('output', filename)
            
            # Add end time to session
            self.current_session['end_time'] = datetime.now().isoformat()
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_session, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Conversation saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")
            raise
            
    def load_conversation(self, filepath: str):
        """Load a conversation from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.current_session = json.load(f)
                
            # Reconstruct conversation history
            self.conversation_history = []
            for msg in self.current_session['messages']:
                self.conversation_history.extend([
                    msg['user_message'],
                    msg['assistant_message']
                ])
                
            logger.info(f"Conversation loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading conversation: {str(e)}")
            raise
            
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation"""
        if not self.current_session:
            return {'status': 'no_active_session'}
            
        return {
            'start_time': self.current_session['start_time'],
            'message_count': len(self.current_session['messages']),
            'total_exchanges': len(self.conversation_history) // 2
        }
        
    def clear_conversation(self):
        """Clear the current conversation"""
        self.conversation_history = []
        self.current_session = None 