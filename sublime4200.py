import argparse
import os

parse = argparse.ArgumentParser()
parse.add_argument('-i', help='Input file', dest='infile')
parse.add_argument('-o', help="Output file", dest='outfile')
args = parse.parse_args()

def replace_hex(infile, outfile, orig, patched):
    # Cek apakah file exists
    if not os.path.exists(infile):
        raise Exception(f"File tidak ditemukan: {infile}")
    
    with open(infile, 'rb') as f: 
        data = bytearray(f.read())
    
    start = data.find(orig)
    if start != -1:
        end = start + len(orig)
        data[start:end] = patched
        with open(outfile, 'wb') as f: 
            f.write(data)
        print(f"File berhasil di-patch: {outfile}")
        return True
    else: 
        return False

def main():
    infile = input("Input file: ").strip('"') if not args.infile else args.infile
    outfile = infile if not args.outfile else args.outfile
    
    # Strip quotes dari path jika ada
    infile = infile.strip('"')
    outfile = outfile.strip('"')
    
    print(f"Mencari pattern di: {infile}")
    
    patterns = [
        (b"\x80\x78\x05\x00\x0F\x94\xC1", b"\xC6\x40\x05\x01\x48\x85\xC9"),
        (b"\x80\x79\x05\x00\x0F\x94\xC2", b"\xC6\x41\x05\x01\xB2\x00\x90"),
        (b"\x0F\xB6\x51\x05\x83\xF2\x01", b"\xC6\x41\x05\x01\xB2\x00\x90")
    ]
    
    success = False
    for i, (orig, patched) in enumerate(patterns, 1):
        try:
            print(f"Mencoba pattern {i}...")
            if replace_hex(infile, outfile, orig, patched):
                success = True
                break
        except Exception as e:
            print(f"Error dengan pattern {i}: {e}")
            continue
    
    if not success:
        print("Error: Tidak ada pattern yang ditemukan dalam file")

if __name__ == "__main__":
    main()