# main.py
import sys
from BST import BST
from search_engine import search_loop

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <wordlist.txt>")
        print("or   : python main.py <url> --url")
        return

    source = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--url":
        bst = BST(source, url=True)
    else:
        bst = BST(source, file=True)

    search_loop(bst)

if __name__ == "__main__":
    main()
