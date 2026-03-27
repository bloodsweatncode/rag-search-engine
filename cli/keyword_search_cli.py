#!/usr/bin/env python3

import argparse
import json
import string


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    fm = open("data/movies.json", "r")
    movies = json.load(fm)

    puncDic = {}
    for punc in string.punctuation:
        puncDic[punc] = None
    puncTrans = str.maketrans(puncDic)

    match args.command:
        case "search":
            results = []
            # print the search query here
            print("Searching for:", args.query)
            for movie in movies["movies"]:
                if args.query.lower().translate(puncTrans) in movie["title"].lower().translate(puncTrans):
                    results.append(movie["title"])
            index = 1
            for result in results[:5]:
                print(str(index) + "." + result)
                index += 1

        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
