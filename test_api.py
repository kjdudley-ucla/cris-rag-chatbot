import json
import pytest
from unittest.mock import patch

def test_chat_endpoint_with_valid_message(client):
    """Test chat endpoint with a valid message."""
    with patch('src.chat.bot.ChatBot.get_response', return_value='Mock response'):
        response = client.post(
            '/api/chat',
            data=json.dumps({'message': 'Test message'}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'response' in data
        assert data['response'] == 'Mock response'

def test_chat_endpoint_without_message(client):
    """Test chat endpoint without providing a message."""
    response = client.post(
        '/api/chat',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == 'No message provided'