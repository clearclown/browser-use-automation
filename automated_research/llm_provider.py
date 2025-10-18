"""
LLM Provider Selection Module
LLMプロバイダー選択モジュール

環境変数に基づいて適切なLLMプロバイダーを自動選択します。
サポート: OpenAI, Claude (Anthropic), DeepSeek, Google Gemini, Groq

Usage:
    from automated_research.llm_provider import get_llm

    # デフォルトモデルで初期化
    llm = get_llm()

    # カスタムモデル指定
    llm = get_llm(model='gpt-4o-mini')

    # プロバイダー明示指定
    llm = get_llm(provider='claude', model='claude-3-5-sonnet-20241022')
"""

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


def get_llm(provider: str | None = None, model: str | None = None, temperature: float = 0.4, **kwargs: Any) -> Any:
	"""
	環境変数に基づいて適切なLLMプロバイダーを取得

	Args:
		provider: LLMプロバイダー名 (openai, claude, deepseek, google, groq)
				  指定しない場合は環境変数 LLM_PROVIDER から取得
		model: モデル名（指定しない場合はプロバイダーのデフォルト）
		temperature: 生成温度（0.0-1.0）
		**kwargs: 追加のLLMパラメータ

	Returns:
		初期化されたLLMインスタンス

	Raises:
		ValueError: サポートされていないプロバイダーまたはAPIキーが設定されていない場合

	環境変数:
		LLM_PROVIDER: 使用するプロバイダー名（デフォルト: openai）
		OPENAI_API_KEY: OpenAI APIキー
		ANTHROPIC_API_KEY: Anthropic (Claude) APIキー
		DEEPSEEK_API_KEY: DeepSeek APIキー
		GOOGLE_API_KEY: Google (Gemini) APIキー
		GROQ_API_KEY: Groq APIキー

	例:
		>>> llm = get_llm()  # LLM_PROVIDER環境変数を使用
		>>> llm = get_llm(provider='claude')
		>>> llm = get_llm(provider='openai', model='gpt-4o-mini')
	"""
	# プロバイダー決定（優先順位: 引数 > 環境変数 > デフォルト）
	if provider is None:
		provider = os.getenv('LLM_PROVIDER', 'openai').lower()

	logger.info(f'Initializing LLM provider: {provider}')

	# プロバイダー別のデフォルトモデル
	default_models = {
		'openai': 'gpt-4o',
		'claude': 'claude-3-5-sonnet-20241022',
		'deepseek': 'deepseek-chat',
		'google': 'gemini-2.0-flash-exp',
		'groq': 'llama-3.3-70b-versatile',
	}

	# モデル決定
	if model is None:
		# 環境変数から取得を試みる
		model_env_map = {
			'openai': 'OPENAI_MODEL',
			'claude': 'CLAUDE_MODEL',
			'deepseek': 'DEEPSEEK_MODEL',
			'google': 'GOOGLE_MODEL',
			'groq': 'GROQ_MODEL',
		}
		model = os.getenv(model_env_map.get(provider, ''), default_models.get(provider, 'gpt-4o'))

	logger.info(f'Using model: {model} with temperature: {temperature}')

	# プロバイダー別にLLMインスタンスを作成
	# Browser-Useの既存LLM統合を使用
	if provider == 'openai':
		from browser_use.llm.openai.chat import ChatOpenAI

		api_key = os.getenv('OPENAI_API_KEY')
		if not api_key:
			raise ValueError('OPENAI_API_KEY environment variable is not set')

		return ChatOpenAI(model=model, temperature=temperature, **kwargs)

	elif provider == 'claude' or provider == 'anthropic':
		# Browser-UseのClaude統合を使用
		try:
			from browser_use.llm.claude.chat import ChatClaude

			api_key = os.getenv('ANTHROPIC_API_KEY')
			if not api_key:
				raise ValueError('ANTHROPIC_API_KEY environment variable is not set')

			return ChatClaude(model=model, temperature=temperature, api_key=api_key, **kwargs)
		except ImportError:
			# Fallback: langchain-anthropicを使用
			try:
				from langchain_anthropic import ChatAnthropic

				api_key = os.getenv('ANTHROPIC_API_KEY')
				if not api_key:
					raise ValueError('ANTHROPIC_API_KEY environment variable is not set')

				return ChatAnthropic(model=model, temperature=temperature, anthropic_api_key=api_key, **kwargs)
			except ImportError:
				raise ImportError(
					'Claude support requires either browser_use.llm.claude or langchain-anthropic. '
					'Install with: pip install langchain-anthropic'
				)

	elif provider == 'deepseek':
		# DeepSeekはOpenAI互換APIを使用
		from browser_use.llm.openai.chat import ChatOpenAI

		api_key = os.getenv('DEEPSEEK_API_KEY')
		if not api_key:
			raise ValueError('DEEPSEEK_API_KEY environment variable is not set')

		# DeepSeek API baseURL
		base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')

		return ChatOpenAI(model=model, temperature=temperature, api_key=api_key, base_url=base_url, **kwargs)

	elif provider == 'google' or provider == 'gemini':
		# Browser-UseのGoogle統合を使用
		try:
			from browser_use.llm.google.chat import ChatGoogle

			api_key = os.getenv('GOOGLE_API_KEY')
			if not api_key:
				raise ValueError('GOOGLE_API_KEY environment variable is not set')

			return ChatGoogle(model=model, temperature=temperature, api_key=api_key, **kwargs)
		except ImportError:
			# Fallback: langchain-google-genaiを使用
			try:
				from langchain_google_genai import ChatGoogleGenerativeAI

				api_key = os.getenv('GOOGLE_API_KEY')
				if not api_key:
					raise ValueError('GOOGLE_API_KEY environment variable is not set')

				return ChatGoogleGenerativeAI(model=model, temperature=temperature, google_api_key=api_key, **kwargs)
			except ImportError:
				raise ImportError(
					'Google support requires either browser_use.llm.google or langchain-google-genai. '
					'Install with: pip install langchain-google-genai'
				)

	elif provider == 'groq':
		# Groq - OpenAI互換APIとして扱う
		from browser_use.llm.openai.chat import ChatOpenAI

		api_key = os.getenv('GROQ_API_KEY')
		if not api_key:
			raise ValueError('GROQ_API_KEY environment variable is not set')

		# Groq API baseURL
		base_url = 'https://api.groq.com/openai/v1'

		return ChatOpenAI(model=model, temperature=temperature, api_key=api_key, base_url=base_url, **kwargs)

	else:
		raise ValueError(
			f'Unsupported LLM provider: {provider}. '
			f'Supported providers: openai, claude, deepseek, google, groq'
		)


def get_available_providers() -> list[str]:
	"""
	環境変数に基づいて利用可能なLLMプロバイダーのリストを取得

	Returns:
		利用可能なプロバイダー名のリスト

	例:
		>>> providers = get_available_providers()
		>>> print(f'Available providers: {", ".join(providers)}')
	"""
	available = []

	if os.getenv('OPENAI_API_KEY'):
		available.append('openai')
	if os.getenv('ANTHROPIC_API_KEY'):
		available.append('claude')
	if os.getenv('DEEPSEEK_API_KEY'):
		available.append('deepseek')
	if os.getenv('GOOGLE_API_KEY'):
		available.append('google')
	if os.getenv('GROQ_API_KEY'):
		available.append('groq')

	return available


def print_provider_info() -> None:
	"""
	現在の設定とAPIキーの有無を表示（デバッグ用）
	"""
	print('\n' + '=' * 60)
	print('LLM Provider Configuration')
	print('=' * 60)

	provider = os.getenv('LLM_PROVIDER', 'openai')
	print(f'Selected Provider: {provider}')

	available = get_available_providers()
	print(f'\nAvailable Providers: {", ".join(available) if available else "None"}')

	print('\nAPI Key Status:')
	print(f'  OpenAI:    {"✓ Set" if os.getenv("OPENAI_API_KEY") else "✗ Not set"}')
	print(f'  Claude:    {"✓ Set" if os.getenv("ANTHROPIC_API_KEY") else "✗ Not set"}')
	print(f'  DeepSeek:  {"✓ Set" if os.getenv("DEEPSEEK_API_KEY") else "✗ Not set"}')
	print(f'  Google:    {"✓ Set" if os.getenv("GOOGLE_API_KEY") else "✗ Not set"}')
	print(f'  Groq:      {"✓ Set" if os.getenv("GROQ_API_KEY") else "✗ Not set"}')

	print('=' * 60 + '\n')


if __name__ == '__main__':
	# デバッグ用: 現在の設定を表示
	from dotenv import load_dotenv

	load_dotenv()

	print_provider_info()

	# 利用可能なプロバイダーで初期化テスト
	available = get_available_providers()
	if available:
		print(f'Testing first available provider: {available[0]}')
		try:
			llm = get_llm(provider=available[0])
			print(f'✓ Successfully initialized {available[0]}')
		except Exception as e:
			print(f'✗ Failed to initialize {available[0]}: {e}')
	else:
		print('⚠ No API keys configured. Please set at least one API key in .env')
