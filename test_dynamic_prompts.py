import os
import logging
from agents.prompt_source_agent import PromptSourceAgent
from agents.prompt_agent import PromptAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_dynamic_prompt_generation():
    """Test dynamic prompt generation and conversation simulation"""
    try:
        # Initialize agents
        source_agent = PromptSourceAgent()
        prompt_agent = PromptAgent()
        
        # Get dynamic prompts from MITRE techniques
        dynamic_prompts = source_agent.get_dynamic_prompts()
        logger.info(f"Generated {len(dynamic_prompts)} dynamic prompts")
        
        if not dynamic_prompts:
            logger.error("No dynamic prompts were generated")
            return False
            
        # Select a random technique-based prompt
        selected_prompt = dynamic_prompts[0]  # Using first prompt for testing
        logger.info(f"Selected prompt: {selected_prompt['content']}")
        
        # Initialize conversation
        conversation = []
        
        # First message - Initial prompt
        initial_prompt = selected_prompt['content']
        conversation.append({"role": "user", "content": initial_prompt})
        logger.info(f"Initial prompt: {initial_prompt}")
        
        # Generate AI response
        ai_response = f"Simulating response to {selected_prompt['tactic']} technique..."
        conversation.append({"role": "assistant", "content": ai_response})
        logger.info(f"AI Response: {ai_response}")
        
        # Second message - Follow-up
        follow_up = prompt_agent.generate_follow_up(conversation)
        conversation.append({"role": "user", "content": follow_up})
        logger.info(f"Follow-up: {follow_up}")
        
        # Generate AI response
        ai_response = "Continuing the simulation with additional details..."
        conversation.append({"role": "assistant", "content": ai_response})
        logger.info(f"AI Response: {ai_response}")
        
        # Third message - Final follow-up
        final_follow_up = prompt_agent.generate_follow_up(conversation)
        conversation.append({"role": "user", "content": final_follow_up})
        logger.info(f"Final follow-up: {final_follow_up}")
        
        # Generate final AI response
        final_response = "Completing the simulation with final details..."
        conversation.append({"role": "assistant", "content": final_response})
        logger.info(f"Final AI Response: {final_response}")
        
        # Save conversation to file
        with open('test_conversation.txt', 'w') as f:
            for message in conversation:
                f.write(f"{message['role']}: {message['content']}\n\n")
        
        logger.info("Test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_dynamic_prompt_generation() 