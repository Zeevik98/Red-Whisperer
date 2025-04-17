import os
import json
import pytest
from datetime import datetime
from conversation_tester import ConversationTester
from agents.chat_injector_agent import ChatInjectorAgent
from agents.prompt_source_agent import PromptSourceAgent

def test_conversation_tester_initialization():
    """Test ConversationTester initialization"""
    tester = ConversationTester()
    assert tester is not None
    assert tester.chat_agent is not None
    assert tester.prompt_agent is not None

def test_static_conversation():
    """Test static conversation flow"""
    tester = ConversationTester()
    result = tester.run_static_conversation_test(
        initial_prompt="Test prompt",
        num_exchanges=2
    )
    
    assert result is not None
    assert result['status'] == 'completed'
    assert result['exchanges'] == 2

def test_dynamic_conversation():
    """Test dynamic conversation flow"""
    tester = ConversationTester()
    context = {
        'topic': 'security',
        'goal': 'test_system',
        'complexity': 'medium'
    }
    
    result = tester.run_dynamic_conversation_test(context)
    
    assert result is not None
    assert result['status'] == 'completed'
    assert result['exchanges'] >= 1

def test_result_saving():
    """Test saving conversation results"""
    tester = ConversationTester()
    test_name = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Run a test
    tester.run_static_conversation_test("Test prompt")
    
    # Save results
    tester.save_results(test_name)
    
    # Check if file exists
    result_file = f"test_results/conversation_{test_name}_*.json"
    import glob
    files = glob.glob(result_file)
    assert len(files) > 0

def test_conversation_analysis():
    """Test conversation analysis"""
    tester = ConversationTester()
    
    # Run a test
    tester.run_static_conversation_test("Test prompt", num_exchanges=2)
    
    # Analyze results
    analysis = tester.analyze_conversation()
    
    assert analysis is not None
    assert 'total_exchanges' in analysis
    assert 'total_tokens' in analysis
    assert analysis['total_exchanges'] == 2 