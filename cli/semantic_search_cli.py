#!/usr/bin/env python3

import argparse

from lib.semantic_search import (
        verify_model,
        embed_text,
        verify_embeddings,
        embed_query_text,
        semantic_search,
        chunk_text,
)

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

    chunk_parser = subparsers.add_parser("chunk", help="Chunks a text")
    chunk_parser.add_argument("text", type=str, help="The text soon to be chunked")
    chunk_parser.add_argument("--chunk_size", type=int, default=200, help="Size of a chunk")

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
            semantic_search(args.query, args.limit)
        case "chunk":
            chunk_text(args.text, args.chunk_size)
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()
