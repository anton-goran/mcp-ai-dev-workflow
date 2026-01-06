#!/usr/bin/env python3
"""
Main script for the MCP project.
Includes download_webpage functionality and minsearch-based document search.
"""

import asyncio
import os
import httpx
import minsearch

async def download_webpage(url: str) -> str:
    """
    Downloads the content of a web page as markdown using Jina reader.

    Args:
        url: The URL of the web page to download

    Returns:
        The markdown content of the web page
    """
    jina_url = f"https://r.jina.ai/{url}"

    async with httpx.AsyncClient() as client:
        response = await client.get(jina_url)
        response.raise_for_status()
        return response.text

def find_md_files(base_path):
    """Find all .md and .mdx files in the base_path directory."""
    md_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(('.md', '.mdx')):
                full_path = os.path.join(root, file)
                # Get relative path from base_path
                rel_path = os.path.relpath(full_path, base_path)
                md_files.append((full_path, rel_path))
    return md_files

def load_documents(base_path):
    """Load documents from md/mdx files."""
    documents = []
    md_files = find_md_files(base_path)

    for full_path, rel_path in md_files:
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            documents.append({
                'content': content,
                'filename': rel_path
            })
        except Exception as e:
            print(f"Error reading {full_path}: {e}")

    return documents

def create_search_index(base_path='fastmcp-main'):
    """Create and return the minsearch index for documents."""
    if not os.path.exists(base_path):
        print(f"Directory {base_path} not found. Please ensure the zip file is unzipped.")
        return None

    documents = load_documents(base_path)
    print(f"Loaded {len(documents)} documents for search")

    index = minsearch.Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    return index

def search_documents(index, query, num_results=5):
    """Search tool: Search the document index and return top results."""
    if index is None:
        return "Search index not available"

    results = index.search(query, num_results=num_results)
    if not results:
        return f"No results found for query: {query}"

    output = f"Search results for '{query}':\n"
    for i, result in enumerate(results, 1):
        output += f"{i}. {result['filename']}\n"
        # Show first 200 chars of content
        content_preview = result['content'][:200].replace('\n', ' ')
        output += f"   Preview: {content_preview}...\n\n"

    return output

# Global search index
search_index = create_search_index()

async def main():
    """Test the download_webpage function and search tool."""
    # Test download_webpage
    test_url = "https://github.com/alexeygrigorev/minsearch"

    print(f"Testing download_webpage with URL: {test_url}")
    print("Fetching content...")

    try:
        content = await download_webpage(test_url)
        print("✅ Success! Content downloaded.")
        print(f"Content length: {len(content)} characters")
        print("\n--- First 500 characters ---")
        print(content[:500])
        print("--- End of preview ---")

        # Check if it looks like markdown
        if content.startswith("#") or "##" in content[:200]:
            print("✅ Content appears to be in markdown format")
        else:
            print("⚠️  Content may not be in expected markdown format")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Test search tool
    print("\n" + "="*50)
    print("Testing Search Tool")
    print("="*50)

    test_queries = ["demo", "getting started", "server"]

    for query in test_queries:
        print(f"\nQuery: {query}")
        result = search_documents(search_index, query, num_results=3)
        print(result)

if __name__ == "__main__":
    asyncio.run(main())