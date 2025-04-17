import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class RecorderAgent:
    def __init__(self, result_dir: str = "test_results"):
        """Initialize the recorder agent with a result directory"""
        self.result_dir = result_dir
        self._ensure_result_dir()
        self.current_session = []
        
    def _ensure_result_dir(self):
        """Ensure the result directory exists"""
        try:
            os.makedirs(self.result_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating result directory: {str(e)}")
            raise
            
    def record_interaction(self, interaction_type: str, content: Dict[str, Any], metadata: Optional[Dict] = None):
        """Record an interaction with timestamp and metadata"""
        try:
            interaction = {
                'timestamp': datetime.now().isoformat(),
                'type': interaction_type,
                'content': content,
                'metadata': metadata or {}
            }
            self.current_session.append(interaction)
            return True
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
            return False
            
    def save_session(self, session_name: str, additional_metadata: Optional[Dict] = None):
        """Save the current session to a file"""
        try:
            if not self.current_session:
                logger.warning("No interactions to save")
                return False
                
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{session_name}_{timestamp}.json"
            filepath = os.path.join(self.result_dir, filename)
            
            session_data = {
                'session_name': session_name,
                'timestamp': timestamp,
                'metadata': additional_metadata or {},
                'interactions': self.current_session
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Session saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving session: {str(e)}")
            return False
            
    def load_session(self, filepath: str) -> Dict[str, Any]:
        """Load a previously saved session"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            return session_data
        except Exception as e:
            logger.error(f"Error loading session from {filepath}: {str(e)}")
            return {}
            
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session"""
        try:
            if not self.current_session:
                return {'status': 'empty', 'interaction_count': 0}
                
            interaction_types = {}
            for interaction in self.current_session:
                int_type = interaction['type']
                interaction_types[int_type] = interaction_types.get(int_type, 0) + 1
                
            return {
                'status': 'active',
                'interaction_count': len(self.current_session),
                'interaction_types': interaction_types,
                'start_time': self.current_session[0]['timestamp'],
                'last_update': self.current_session[-1]['timestamp']
            }
            
        except Exception as e:
            logger.error(f"Error getting session summary: {str(e)}")
            return {'status': 'error', 'message': str(e)}
            
    def clear_session(self):
        """Clear the current session data"""
        try:
            self.current_session = []
            return True
        except Exception as e:
            logger.error(f"Error clearing session: {str(e)}")
            return False
            
    def get_interactions_by_type(self, interaction_type: str) -> List[Dict[str, Any]]:
        """Get all interactions of a specific type"""
        try:
            return [
                interaction for interaction in self.current_session
                if interaction['type'] == interaction_type
            ]
        except Exception as e:
            logger.error(f"Error filtering interactions: {str(e)}")
            return []
            
    def export_session_csv(self, filepath: str) -> bool:
        """Export the current session to CSV format"""
        try:
            import pandas as pd
            
            if not self.current_session:
                logger.warning("No interactions to export")
                return False
                
            # Convert session data to DataFrame
            df = pd.DataFrame(self.current_session)
            
            # Export to CSV
            df.to_csv(filepath, index=False)
            logger.info(f"Session exported to CSV: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting session to CSV: {str(e)}")
            return False 