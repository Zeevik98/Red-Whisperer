import os
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from conversation_tester import ConversationTester
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
load_dotenv()

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='AI Security Testing Framework')
    parser.add_argument('--task-card', type=str, help='Path to TaskCard JSON file for A2A mode')
    parser.add_argument('--a2a-mode', action='store_true', help='Enable A2A mode')
    parser.add_argument('--config', type=str, default='test_config.json', help='Path to test configuration file')
    return parser.parse_args()

def load_task_card(task_card_path: str) -> Optional[Dict[str, Any]]:
    """Load A2A task card from file"""
    if not task_card_path:
        return None
    try:
        with open(task_card_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading task card: {str(e)}")
        return None

def load_test_config(config_file: str = 'test_config.json'):
    """Load test configuration from file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading test config: {str(e)}")
        return None

def run_tests(config):
    """Run tests based on configuration"""
    try:
        tester = ConversationTester()
        
        # Create results directory
        os.makedirs(config['configuration']['result_directory'], exist_ok=True)
        
        # Run each test
        for test in config['tests']:
            logger.info(f"Running test: {test['id']}")
            
            if test['type'] == 'static':
                result = tester.run_static_conversation_test(
                    initial_prompt=test['prompt'],
                    num_exchanges=test.get('num_exchanges', 3)
                )
            else:  # dynamic
                result = tester.run_dynamic_conversation_test(
                    context=test['context']
                )
                
            # Save test results
            if config['configuration']['save_results']:
                tester.save_results(test['id'])
                
            logger.info(f"Test {test['id']} completed with status: {result['status']}")
            
    except Exception as e:
        logger.error(f"Error running tests: {str(e)}")
        return False
        
    return True

def process_a2a_task(task_card: Dict[str, Any]) -> Dict[str, Any]:
    """Process task in A2A mode"""
    try:
        tester = ConversationTester()
        
        # Process the task based on task card type
        if task_card.get('type') == 'security_test':
            result = tester.run_dynamic_conversation_test(
                context=task_card.get('context', {})
            )
        else:
            result = tester.run_static_conversation_test(
                initial_prompt=task_card.get('prompt', ''),
                num_exchanges=task_card.get('num_exchanges', 3)
            )
            
        # Prepare A2A response
        response = {
            'task_id': task_card.get('id'),
            'timestamp': datetime.now().isoformat(),
            'status': 'completed',
            'result': result
        }
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing A2A task: {str(e)}")
        return {
            'task_id': task_card.get('id'),
            'timestamp': datetime.now().isoformat(),
            'status': 'failed',
            'error': str(e)
        }

def main():
    """Main entry point"""
    try:
        args = parse_args()
        
        # Ensure output directories exist
        os.makedirs('logs', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        
        if args.task_card or args.a2a_mode:
            # A2A mode
            task_card = load_task_card(args.task_card)
            if not task_card:
                logger.error("Failed to load task card")
                return
                
            result = process_a2a_task(task_card)
            
            # Save A2A result
            output_path = Path("output") / f"{task_card['id']}_result.json"
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
                
            logger.info(f"A2A task completed. Result saved to {output_path}")
            
        else:
            # Standalone mode
            config = load_test_config(args.config)
            if not config:
                logger.error("Failed to load configuration")
                return
                
            success = run_tests(config)
            if success:
                logger.info("All tests completed successfully")
            else:
                logger.error("Some tests failed")
                
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 