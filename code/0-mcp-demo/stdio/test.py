#!/usr/bin/env python3
"""
Test script for the download_webpage functionality.
This script tests the Jina reader integration by downloading web page content.
"""

import asyncio
import httpx

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

async def main():
    """Test the download_webpage function with a sample URL."""
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

if __name__ == "__main__":
    asyncio.run(main())