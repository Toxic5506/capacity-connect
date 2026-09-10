import sys, base64

def main():
    if len(sys.argv) < 2:
        print("Usage: python writer.py <dest_file>")
        return
    dest = sys.argv[1]
    encoded = sys.stdin.read()
    raw = base64.b64decode(encoded.strip().encode('utf-8'))
    with open(dest, 'wb') as f:
        f.write(raw)
    print(f"Wrote {len(raw)} bytes to {dest}")

if __name__ == '__main__':
    main()
