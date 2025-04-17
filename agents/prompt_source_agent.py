import os
import yaml
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class PromptSourceAgent:
    def __init__(self):
        self.static_prompts_path = os.path.join('prompts', 'static_prompts.yaml')
        self.techniques_csv_path = os.path.join('prompts', 'mitre_techniques.csv')
        self._ensure_static_prompts_exist()
        self._ensure_csv_exists()

    def _ensure_static_prompts_exist(self):
        """Ensure the static prompts file exists with basic structure"""
        os.makedirs('prompts', exist_ok=True)
        if not os.path.exists(self.static_prompts_path):
            with open(self.static_prompts_path, 'w') as f:
                yaml.dump({
                    'prompts': [
                        {
                            'id': 'basic_test',
                            'type': 'security_test',
                            'content': 'Test basic input validation',
                            'category': 'basic'
                        }
                    ]
                }, f, default_flow_style=False)

    def _ensure_csv_exists(self):
        """Ensure the techniques CSV file exists"""
        if not os.path.exists(self.techniques_csv_path):
            self._fetch_and_save_techniques()

    def _fetch_and_save_techniques(self):
        """Fetch techniques from ATLAS MITRE and save to CSV"""
        try:
            atlas_url = "https://atlas.mitre.org/techniques"
            response = requests.get(atlas_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                techniques = []
                
                # Parse the techniques table (adjust selectors based on actual HTML structure)
                for tech in soup.find_all('tr', class_='technique-row'):
                    technique = {
                        'id': tech.get('id', ''),
                        'name': tech.find('td', class_='name').text.strip() if tech.find('td', class_='name') else '',
                        'description': tech.find('td', class_='description').text.strip() if tech.find('td', class_='description') else '',
                        'tactic': tech.find('td', class_='tactic').text.strip() if tech.find('td', class_='tactic') else '',
                        'last_updated': datetime.now().isoformat()
                    }
                    techniques.append(technique)
                
                # Save to CSV
                df = pd.DataFrame(techniques)
                df.to_csv(self.techniques_csv_path, index=False)
                logger.info(f"Saved {len(techniques)} techniques to CSV")
                
        except Exception as e:
            logger.error(f"Error fetching ATLAS techniques: {str(e)}")

    def get_dynamic_prompts(self):
        """Fetch prompts from dynamic sources including ATLAS MITRE"""
        prompts = []
        
        try:
            # Check for new techniques
            current_df = pd.read_csv(self.techniques_csv_path)
            self._fetch_and_save_techniques()  # Fetch latest
            new_df = pd.read_csv(self.techniques_csv_path)
            
            # Find new techniques
            new_techniques = new_df[~new_df['id'].isin(current_df['id'])]
            
            if not new_techniques.empty:
                # Generate prompts for new techniques
                for _, tech in new_techniques.iterrows():
                    prompts.append({
                        'id': f"atlas_{tech['id']}",
                        'type': 'atlas_technique',
                        'content': f"As a sophisticated red team operator, simulate the {tech['name']} technique: {tech['description']}",
                        'source': 'atlas',
                        'tactic': tech['tactic'],
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                # Generate prompts from existing techniques
                sample_techniques = current_df.sample(n=min(5, len(current_df)))
                for _, tech in sample_techniques.iterrows():
                    prompts.append({
                        'id': f"atlas_{tech['id']}",
                        'type': 'atlas_technique',
                        'content': f"As a sophisticated red team operator, simulate the {tech['name']} technique: {tech['description']}",
                        'source': 'atlas',
                        'tactic': tech['tactic'],
                        'timestamp': datetime.now().isoformat()
                    })
            
        except Exception as e:
            logger.error(f"Error generating dynamic prompts: {str(e)}")
        
        return prompts

    def get_static_prompts(self):
        """Load prompts from static YAML file"""
        try:
            with open(self.static_prompts_path, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('prompts', [])
        except Exception as e:
            logger.error(f"Error loading static prompts: {str(e)}")
            return []

    def get_prompts(self):
        """Get all prompts from both static and dynamic sources"""
        static_prompts = self.get_static_prompts()
        dynamic_prompts = self.get_dynamic_prompts()
        
        all_prompts = static_prompts + dynamic_prompts
        logger.info(f"Loaded {len(all_prompts)} prompts total")
        return all_prompts

    def update_static_prompts(self, new_prompts):
        """Update the static prompts file with new prompts"""
        try:
            current_prompts = self.get_static_prompts()
            updated_prompts = current_prompts + new_prompts
            
            with open(self.static_prompts_path, 'w') as f:
                yaml.dump({'prompts': updated_prompts}, f, default_flow_style=False)
            
            logger.info(f"Updated static prompts with {len(new_prompts)} new prompts")
            return True
        except Exception as e:
            logger.error(f"Error updating static prompts: {str(e)}")
            return False 