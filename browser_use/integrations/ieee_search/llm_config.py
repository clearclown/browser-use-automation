"""
LLM Configuration Helper for IEEE Paper Search Tool.
Supports multiple LLM providers: Claude, OpenAI, DeepSeek, Google, Grok.
"""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def get_llm_from_env() -> Any:
	"""
	Initialize LLM based on environment variables.

	Environment variables:
		LLM_PROVIDER: Provider name (claude, openai, deepseek, google, grok)
		ANTHROPIC_API_KEY: Claude API key
		OPENAI_API_KEY: OpenAI API key
		DEEPSEEK_API_KEY: DeepSeek API key
		GOOGLE_API_KEY: Google API key
		GROK_API_KEY: Grok API key

	Returns:
		LLM instance configured for the selected provider

	Raises:
		ValueError: If provider is not supported or API key is missing
	"""
	provider = os.getenv('LLM_PROVIDER', 'claude').lower()
	logger.info(f'🤖 Initializing LLM provider: {provider}')

	if provider == 'claude':
		api_key = os.getenv('ANTHROPIC_API_KEY')
		if not api_key:
			raise ValueError('ANTHROPIC_API_KEY not found in environment variables')

		from langchain_anthropic import ChatAnthropic

		model = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-20250514')
		logger.info(f'✅ Using Claude model: {model}')
		return ChatAnthropic(api_key=api_key, model=model, timeout=25, stop=None)

	elif provider == 'openai':
		api_key = os.getenv('OPENAI_API_KEY')
		if not api_key:
			raise ValueError('OPENAI_API_KEY not found in environment variables')

		from langchain_openai import ChatOpenAI

		model = os.getenv('OPENAI_MODEL', 'gpt-4o')
		logger.info(f'✅ Using OpenAI model: {model}')
		return ChatOpenAI(api_key=api_key, model=model, timeout=25, stop=None)

	elif provider == 'deepseek':
		api_key = os.getenv('DEEPSEEK_API_KEY')
		if not api_key:
			raise ValueError('DEEPSEEK_API_KEY not found in environment variables')

		from langchain_openai import ChatOpenAI

		model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
		logger.info(f'✅ Using DeepSeek model: {model}')
		return ChatOpenAI(
			api_key=api_key, model=model, base_url='https://api.deepseek.com', timeout=25, stop=None
		)

	elif provider == 'google':
		api_key = os.getenv('GOOGLE_API_KEY')
		if not api_key:
			raise ValueError('GOOGLE_API_KEY not found in environment variables')

		from langchain_google_genai import ChatGoogleGenerativeAI

		model = os.getenv('GOOGLE_MODEL', 'gemini-2.0-flash-exp')
		logger.info(f'✅ Using Google model: {model}')
		return ChatGoogleGenerativeAI(api_key=api_key, model=model, timeout=25, stop=None)

	elif provider == 'grok':
		api_key = os.getenv('GROK_API_KEY')
		if not api_key:
			raise ValueError('GROK_API_KEY not found in environment variables')

		from langchain_openai import ChatOpenAI

		model = os.getenv('GROK_MODEL', 'grok-3')
		logger.info(f'✅ Using Grok model: {model}')
		return ChatOpenAI(api_key=api_key, model=model, base_url='https://api.x.ai/v1', timeout=25, stop=None)

	else:
		raise ValueError(
			f'Unsupported LLM provider: {provider}. '
			f'Supported providers: claude, openai, deepseek, google, grok'
		)
