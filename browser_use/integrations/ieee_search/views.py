"""
Data models for IEEE paper search integration.
"""

from pydantic import BaseModel, Field


class Citation(BaseModel):
	"""Citation/excerpt from a paper with source tracking."""

	text: str = Field(description='Quoted text from the paper')
	paper_title: str = Field(description='Title of the source paper')
	paper_url: str = Field(description='URL of the source paper')
	page_number: int | None = Field(default=None, description='Page number where the quote appears')
	section: str | None = Field(default=None, description='Section name (e.g., Abstract, Introduction)')
	authors: list[str] = Field(default_factory=list, description='Paper authors')
	notes: str | None = Field(default=None, description='User notes about this citation')


class PaperMetadata(BaseModel):
	"""Metadata for an academic paper."""

	title: str = Field(description='Paper title')
	authors: list[str] = Field(default_factory=list, description='List of authors')
	url: str = Field(description='Paper URL')
	doi: str | None = Field(default=None, description='Digital Object Identifier')
	year: int | None = Field(default=None, description='Publication year')
	abstract: str | None = Field(default=None, description='Paper abstract')
	citations: list[Citation] = Field(default_factory=list, description='Extracted citations/excerpts')


class SearchProgress(BaseModel):
	"""Progress information for search operations."""

	current_paper: int = Field(description='Current paper index being processed')
	total_papers: int = Field(description='Total number of papers to process')
	status: str = Field(description='Current status message')
	papers_processed: list[str] = Field(default_factory=list, description='Titles of processed papers')
