#!/usr/bin/env python3

import argparse

from lib.semantic_search import (
        verify_model,
        embed_text,
        verify_embeddings,
        embed_query_text,
        SemanticSearch,
)

from lib.search_utils import load_movies

def main():
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("verify", help="Verify loaded model and max sequenze length")

    single_embed_parser = subparsers.add_parser("embed_text", help="Generate an embedding for a single text")
    single_embed_parser.add_argument("text", type=str, help="Text to embed")

    verify_embeddings_parser = subparsers.add_parser("verify_embeddings", help="Kunibert")

    embedquery_parser = subparsers.add_parser("embedquery")
    embedquery_parser.add_argument("query", type=str)

    search_parser = subparsers.add_parser("search", help="Search for movies using semantic search")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--limit", type=int, default=5,  help="Number of results to return")

    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case "verify_embeddings":
            verify_embeddings()
        case "embedquery":
            embed_query_text(args.query)
        case "search":
            ses = SemanticSearch()
            movies = load_movies()
            ses.load_or_create_embeddings(movies)
            search_results = ses.search(args.query, args.limit)
            for i, search_result in enumerate(search_results, 1):
                print(f"{i}. {search_result['title']} (score: {search_result['score']:.4f})") 
                print(f"{search_result['description'][:100]}...\n")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
