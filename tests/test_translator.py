"""
Test Cases for Multilingual Ticket Translator
Covers: language detection, translation, glossary handling, agent loop, reply flow
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest

# ─── Glossary Tests ───────────────────────────────────────────────────────────

from glossary import apply_glossary, restore_glossary, GLOSSARY

def test_glossary_protects_api():
    text = "The API is returning error 404"
    protected, placeholders = apply_glossary(text)
    assert "API" not in protected or "__TERM" in protected
    restored = restore_glossary(protected, placeholders)
    assert "API" in restored
    assert "error 404" in restored

def test_glossary_round_trip():
    text = "Please check the dashboard and try login again"
    protected, placeholders = apply_glossary(text)
    restored = restore_glossary(protected, placeholders)
    assert restored == text

def test_glossary_no_false_positives():
    text = "I love this product so much"
    protected, placeholders = apply_glossary(text)
    assert len(placeholders) == 0
    assert protected == text

# ─── Language Detection Tests ─────────────────────────────────────────────────

from unittest.mock import patch

def test_detect_english():
    from translator import detect_language
    lang = detect_language("I cannot login to my account")
    assert lang == 'en'

def test_detect_hindi():
    from translator import detect_language
    lang = detect_language("मेरा खाता काम नहीं कर रहा है")
    assert lang == 'hi'

def test_detect_french():
    from translator import detect_language
    lang = detect_language("Je ne peux pas me connecter")
    assert lang == 'fr'

# ─── Agent Happy Path Tests ───────────────────────────────────────────────────

from unittest.mock import patch, MagicMock

def test_agent_english_ticket_skips_translation():
    """English tickets should skip translation step."""
    with patch('agent.save_ticket') as mock_save:
        from agent import process_ticket_agent
        result = process_ticket_agent("My login is broken and the dashboard shows error 404")
        assert result['original_lang'] == 'en'
        assert result['english_text'] == result['original_text']
        steps = [s['step'] for s in result['agent_steps']]
        assert 'detect_language' in steps
        assert 'store_ticket' in steps
        mock_save.assert_called()

def test_agent_produces_required_fields():
    """Every processed ticket must have these fields."""
    with patch('agent.save_ticket'):
        from agent import process_ticket_agent
        result = process_ticket_agent("Test ticket")
        assert 'ticket_id' in result
        assert 'original_lang' in result
        assert 'original_text' in result
        assert 'english_text' in result
        assert 'agent_steps' in result

def test_reply_translates_back():
    """Reply must be translated back to original language."""
    fake_ticket = {
        'ticket_id': 'abc123',
        'original_lang': 'fr',
        'original_text': 'Bonjour, je ne peux pas me connecter.',
        'english_text': 'Hello, I cannot login.',
        'status': 'open'
    }
    with patch('agent.get_ticket', return_value=fake_ticket), \
         patch('agent.save_ticket'), \
         patch('agent.translate_from_english', return_value='Votre problème a été résolu.') as mock_trans:
        from agent import reply_to_user
        result = reply_to_user('abc123', 'Your issue has been resolved.')
        assert result['original_lang'] == 'fr'
        assert 'translated_reply' in result
        mock_trans.assert_called_once()

def test_reply_english_ticket_no_translation():
    """Replies to English tickets should not be translated."""
    fake_ticket = {
        'ticket_id': 'xyz999',
        'original_lang': 'en',
        'original_text': 'My API is broken',
        'english_text': 'My API is broken',
        'status': 'open'
    }
    with patch('agent.get_ticket', return_value=fake_ticket), \
         patch('agent.save_ticket'):
        from agent import reply_to_user
        result = reply_to_user('xyz999', 'We have fixed the API issue.')
        assert result['translated_reply'] == 'We have fixed the API issue.'

def test_reply_missing_ticket_raises():
    """Replying to a non-existent ticket should raise ValueError."""
    with patch('agent.get_ticket', return_value=None):
        from agent import reply_to_user
        with pytest.raises(ValueError):
            reply_to_user('nonexistent', 'Hello')
