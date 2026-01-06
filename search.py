#!/usr/bin/env python3
"""
Search implementation using minsearch to index markdown files from fastmcp repository.
"""

import os
import minsearch

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

def create_index(documents):
    """Create and fit the minsearch index."""
    index = minsearch.Index(
        text_fields=['content'],
        keyword_fields=['filename']
    )
    index.fit(documents)
    return index

def search_documents(index, query, num_results=5):
    """Search the index and return top results."""
    return index.search(query, num_results=num_results)

def main():
    """Test the search implementation."""
    base_path = 'fastmcp-main'

    if not os.path.exists(base_path):
        print(f"Directory {base_path} not found. Please ensure the zip file is unzipped.")
        return

    print("Loading documents...")
    documents = load_documents(base_path)
    print(f"Loaded {len(documents)} documents")

    print("Creating index...")
    index = create_index(documents)
    print("Index created")

    # Test search
    test_queries = [
        "getting started",
        "server",
        "client",
        "tool",
        "demo"
    ]

    for query in test_queries:
        print(f"\nSearch results for '{query}':")
        results = search_documents(index, query)
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['filename']} (score: {result.get('score', 'N/A')})")
            # Show first 100 chars of content
            content_preview = result['content'][:100].replace('\n', ' ')
            print(f"   Preview: {content_preview}...")

if __name__ == "__main__":
    main()