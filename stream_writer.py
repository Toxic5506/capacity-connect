import sys

def main():
    target = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'a'
    data = sys.stdin.read()
    with open(target, mode, encoding='utf-8') as f:
        f.write(data)

if __name__ == '__main__':
    main()
