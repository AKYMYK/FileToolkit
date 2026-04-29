"""
Command-line interface for FileToolkit.
"""
import argparse
import sys
from .encryptor import encrypt_file, decrypt_file
from .converter import convert_encoding
from .renamer import batch_rename

def main():
    parser = argparse.ArgumentParser(description="FileToolkit - multi-function file utility")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # encrypt
    enc_parser = subparsers.add_parser('encrypt', help='Encrypt a file')
    enc_parser.add_argument('--input', required=True)
    enc_parser.add_argument('--output', required=True)
    enc_parser.add_argument('--password', required=True)

    # decrypt
    dec_parser = subparsers.add_parser('decrypt', help='Decrypt a file')
    dec_parser.add_argument('--input', required=True)
    dec_parser.add_argument('--output', required=True)
    dec_parser.add_argument('--password', required=True)

    # convert
    conv_parser = subparsers.add_parser('convert', help='Convert file encoding')
    conv_parser.add_argument('--input', required=True)
    conv_parser.add_argument('--output', required=True)
    conv_parser.add_argument('--from', dest='from_enc')
    conv_parser.add_argument('--to', default='utf-8')

    # rename
    ren_parser = subparsers.add_parser('rename', help='Batch rename files')
    ren_parser.add_argument('--folder', required=True)
    ren_parser.add_argument('--prefix', default='')
    ren_parser.add_argument('--suffix', default='')
    ren_parser.add_argument('--replace-old')
    ren_parser.add_argument('--replace-new')
    ren_parser.add_argument('--regex-pattern')
    ren_parser.add_argument('--regex-repl')
    ren_parser.add_argument('--start-index', type=int, default=1)
    ren_parser.add_argument('--preview', action='store_true')

    args = parser.parse_args()

    if args.command == 'encrypt':
        success = encrypt_file(args.input, args.output, args.password)
    elif args.command == 'decrypt':
        success = decrypt_file(args.input, args.output, args.password)
    elif args.command == 'convert':
        success = convert_encoding(args.input, args.output,
                                   args.from_enc, args.to)
    elif args.command == 'rename':
        success = batch_rename(args.folder, args.prefix, args.suffix,
                               args.replace_old, args.replace_new,
                               args.regex_pattern, args.regex_repl,
                               args.start_index, args.preview)
    else:
        success = False

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
