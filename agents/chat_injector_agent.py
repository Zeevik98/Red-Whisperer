import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class MockOpenAI:
    """Mock OpenAI client for testing"""
    def chat_completions_create(self, *args, **kwargs):
        return type('MockResponse', (), {
            'choices': [type('MockChoice', (), {
                'message': {'content': 'This is a mock response'}
            })()],
            'created': 123456789
        })()

class ChatInjectorAgent:
    """Agent for testing chat systems using AI-generated prompts."""
    
    def __init__(self):
        """Initialize the ChatInjectorAgent with OpenAI client."""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
            api_key = "test_key_for_unit_tests"
        
        try:
            self.client = OpenAI(api_key=api_key)
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            self.client = MockOpenAI()

    def execute_injection(self, chat_elements: dict, prompt: dict, target_url: str) -> dict:
        """Execute a prompt injection test.
        
        Args:
            chat_elements: Dictionary containing chat interface elements
            prompt: Dictionary containing prompt type and content
            target_url: URL of the target system
            
        Returns:
            Dictionary containing test results and generated content
        """
        try:
            # Prepare the injection context
            context = {
                'target_url': target_url,
                'chat_elements': chat_elements,
                'prompt_type': prompt.get('type', 'unknown')
            }
            
            # Get GPT-4 response
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a security researcher testing chat systems."},
                    {"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt['content']}"}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract the generated text
            generated_text = response.choices[0].message.content
            
            # Prepare result
            result = {
                'prompt': prompt,
                'generated_text': generated_text,
                'context': context,
                'model': 'gpt-4',
                'timestamp': response.created
            }
            
            logger.info(f"Successfully generated injection for {target_url}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing injection: {str(e)}")
            raise 