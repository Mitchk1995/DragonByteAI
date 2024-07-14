import json

class ResponseParser:
    @staticmethod
    def parse_quest(response):
        try:
            quest_data = json.loads(response)
            return {
                'title': quest_data['title'],
                'description': quest_data['description'],
                'objectives': quest_data['objectives'],
                'reward': quest_data['reward']
            }
        except json.JSONDecodeError:
            return {'error': 'Failed to parse quest data'}

    @staticmethod
    def parse_dialogue(response):
        lines = response.split('\n')
        dialogue = []
        for line in lines:
            if ':' in line:
                speaker, text = line.split(':', 1)
                dialogue.append({'speaker': speaker.strip(), 'text': text.strip()})
        return dialogue

    @staticmethod
    def parse_combat_narration(response):
        return {
            'narration': response.strip(),
            'outcome': 'victory' if 'victory' in response.lower() else 'defeat'
        }
