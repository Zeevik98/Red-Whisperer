import logging
from typing import Dict, Any, List, Optional
import random

logger = logging.getLogger(__name__)

class PromptAgent:
    def __init__(self, base_prompts: Optional[List[str]] = None):
        """Initialize the prompt agent with optional base prompts"""
        self.base_prompts = base_prompts or []
        self.prompt_history = []
        self.context = {}
        
    def add_base_prompt(self, prompt: str):
        """Add a new base prompt to the collection"""
        try:
            if prompt not in self.base_prompts:
                self.base_prompts.append(prompt)
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding base prompt: {str(e)}")
            return False
            
    def generate_prompt(self, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a prompt based on context and base prompts"""
        try:
            if not self.base_prompts:
                raise ValueError("No base prompts available")
                
            selected_prompt = random.choice(self.base_prompts)
            
            if context:
                # Update context
                self.context.update(context)
                
                # Format prompt with context
                try:
                    formatted_prompt = selected_prompt.format(**self.context)
                except KeyError as e:
                    logger.warning(f"Missing context key: {str(e)}")
                    formatted_prompt = selected_prompt
            else:
                formatted_prompt = selected_prompt
                
            self.prompt_history.append({
                'base_prompt': selected_prompt,
                'formatted_prompt': formatted_prompt,
                'context': context
            })
            
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Error generating prompt: {str(e)}")
            return ""
            
    def get_prompt_history(self) -> List[Dict[str, Any]]:
        """Get the history of generated prompts"""
        return self.prompt_history
        
    def clear_history(self):
        """Clear the prompt history"""
        try:
            self.prompt_history = []
            return True
        except Exception as e:
            logger.error(f"Error clearing history: {str(e)}")
            return False
            
    def update_context(self, new_context: Dict[str, Any]):
        """Update the current context"""
        try:
            self.context.update(new_context)
            return True
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            return False
            
    def clear_context(self):
        """Clear the current context"""
        try:
            self.context = {}
            return True
        except Exception as e:
            logger.error(f"Error clearing context: {str(e)}")
            return False
            
    def get_context(self) -> Dict[str, Any]:
        """Get the current context"""
        return self.context
        
    def remove_base_prompt(self, prompt: str) -> bool:
        """Remove a base prompt from the collection"""
        try:
            if prompt in self.base_prompts:
                self.base_prompts.remove(prompt)
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing base prompt: {str(e)}")
            return False
            
    def get_base_prompts(self) -> List[str]:
        """Get all base prompts"""
        return self.base_prompts
        
    def generate_follow_up(self, previous_response: str) -> str:
        """Generate a follow-up prompt based on the previous response"""
        try:
            # Simple follow-up generation logic
            follow_up_templates = [
                "Can you elaborate on {}?",
                "Tell me more about {}.",
                "What are the implications of {}?",
                "How does {} relate to the original context?"
            ]
            
            # Extract key phrases or use the first sentence
            key_phrase = previous_response.split('.')[0]
            
            # Generate follow-up
            follow_up = random.choice(follow_up_templates).format(key_phrase)
            
            self.prompt_history.append({
                'type': 'follow_up',
                'previous_response': previous_response,
                'generated_follow_up': follow_up
            })
            
            return follow_up
            
        except Exception as e:
            logger.error(f"Error generating follow-up: {str(e)}")
            return "" 