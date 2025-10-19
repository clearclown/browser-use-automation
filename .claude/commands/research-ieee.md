# IEEE Research Command

Search IEEE Xplore for academic papers and extract structured data.

## Usage

```
/research-ieee <search query> [options]
```

## Task

You are to conduct a comprehensive search on IEEE Xplore for papers related to the given search query.

**Steps:**

1. **Delegate to ieee-researcher agent**: Use the `ieee-researcher` subagent to:
   - Navigate to IEEE Xplore
   - Perform the search with the given query
   - Apply relevant filters (recent years, document type, etc.)
   - Extract metadata from search results (title, authors, DOI, abstract, year)
   - Handle pagination to collect multiple results

2. **Structure Results**: Organize the findings into a structured JSON format

3. **Summary**: Provide a brief summary of:
   - Total results found
   - Number of papers extracted
   - Year range of papers
   - Key topics identified

4. **Save Results** (optional): If requested, save results to a JSON file

## Expected Output

```json
{
  "query": "search terms",
  "search_date": "2024-01-01",
  "total_results": 150,
  "papers_extracted": 20,
  "papers": [
    {
      "title": "Paper Title",
      "authors": ["Author 1", "Author 2"],
      "year": 2024,
      "doi": "10.1109/XXXXX",
      "abstract": "Abstract text...",
      "url": "https://ieeexplore.ieee.org/document/XXXXX",
      "publication": "Conference/Journal Name",
      "citations": 42
    }
  ],
  "summary": {
    "year_range": "2020-2024",
    "top_keywords": ["keyword1", "keyword2"],
    "document_types": {
      "conference": 15,
      "journal": 5
    }
  }
}
```

## Options

- `--limit <n>`: Limit to n results (default: 20)
- `--years <range>`: Filter by year range (e.g., "2020-2024")
- `--type <type>`: Filter by document type (conference, journal, magazine)
- `--save <filename>`: Save results to JSON file

## Examples

```bash
# Basic search
/research-ieee machine learning robotics

# Search with year filter
/research-ieee deep learning --years 2022-2024

# Search with result limit
/research-ieee neural networks --limit 50

# Search and save
/research-ieee computer vision --save cv_papers.json
```

## Notes

- This command delegates to the ieee-researcher subagent
- Results are cached to avoid redundant searches
- Respect IEEE's rate limits and terms of service
- Some papers may require subscription access
