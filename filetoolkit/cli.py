"""
Command-line interface for FileToolkit.
Provides subcommands: encrypt, decrypt, convert, rename, hash, split, merge, backup.
"""
import argparse
import sys
import os
from .encryptor import encrypt_file, decrypt_file
from .converter import convert_encoding
from .renamer import batch_rename
from .hasher import compute_hash, verify_hash
from .splitter import split_by_size, split_by_parts, merge_files
from .backup import backup_file, backup_directory

def main():
    parser = argparse.ArgumentParser(
        description="FileToolkit - A multi-function file utility",
        epilog="See 'filetoolkit <command> --help' for more info on each command."
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # ---------- encrypt ----------
    enc_parser = subparsers.add_parser('encrypt', help='Encrypt a file using AES')
    enc_parser.add_argument('--input', required=True, help='Path to input file')
    enc_parser.add_argument('--output', required=True, help='Path to encrypted output file')
    enc_parser.add_argument('--password', required=True, help='Encryption password')

    # ---------- decrypt ----------
    dec_parser = subparsers.add_parser('decrypt', help='Decrypt a file (AES)')
    dec_parser.add_argument('--input', required=True, help='Path to encrypted file')
    dec_parser.add_argument('--output', required=True, help='Path to decrypted output file')
    dec_parser.add_argument('--password', required=True, help='Decryption password')

    # ---------- convert ----------
    conv_parser = subparsers.add_parser('convert', help='Convert file encoding')
    conv_parser.add_argument('--input', required=True, help='Input file')
    conv_parser.add_argument('--output', required=True, help='Output file')
    conv_parser.add_argument('--from', dest='from_enc', help='Source encoding (auto-detect if omitted)')
    conv_parser.add_argument('--to', default='utf-8', help='Target encoding (default: utf-8)')

    # ---------- rename ----------
    ren_parser = subparsers.add_parser('rename', help='Batch rename files in a folder')
    ren_parser.add_argument('--folder', required=True, help='Target folder')
    ren_parser.add_argument('--prefix', default='', help='Rename prefix')
    ren_parser.add_argument('--suffix', default='', help='Rename suffix')
    ren_parser.add_argument('--replace-old', help='Text to replace')
    ren_parser.add_argument('--replace-new', help='Replacement text')
    ren_parser.add_argument('--regex-pattern', help='Regex pattern (for replacement)')
    ren_parser.add_argument('--regex-repl', help='Regex replacement')
    ren_parser.add_argument('--start-index', type=int, default=1, help='Starting index number')
    ren_parser.add_argument('--preview', action='store_true', help='Preview changes without renaming')

    # ---------- hash ----------
    hash_parser = subparsers.add_parser('hash', help='Compute file hash')
    hash_parser.add_argument('--input', required=True, help='File to hash')
    hash_parser.add_argument('--algorithm', default='sha256',
                             choices=['md5', 'sha1', 'sha256', 'sha512'],
                             help='Hash algorithm (default: sha256)')

    # ---------- split ----------
    split_parser = subparsers.add_parser('split', help='Split a file into parts')
    split_parser.add_argument('--input', required=True, help='File to split')
    split_parser.add_argument('--output-dir', default=None, help='Output directory')
    mode = split_parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--size', type=int, help='Size of each part in bytes')
    mode.add_argument('--parts', type=int, help='Number of equal-sized parts')

    # ---------- merge ----------
    merge_parser = subparsers.add_parser('merge', help='Merge file parts')
    merge_parser.add_argument('--parts', nargs='+', required=True, help='Part files (in order)')
    merge_parser.add_argument('--output', required=True, help='Merged output file')

    # ---------- backup ----------
    backup_parser = subparsers.add_parser('backup', help='Backup a file or directory')
    backup_parser.add_argument('--input', required=True, help='File or directory to backup')
    backup_parser.add_argument('--backup-dir', default='./backup', help='Backup directory')
    backup_parser.add_argument('--no-timestamp', action='store_true', help='Do not append timestamp')

    args = parser.parse_args()

    success = False

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
    elif args.command == 'hash':
        try:
            result = compute_hash(args.input, args.algorithm)
            print(result)
            success = True
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == 'split':
        try:
            if args.size:
                success = split_by_size(args.input, args.size, args.output_dir)
            else:
                success = split_by_parts(args.input, args.parts, args.output_dir)
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == 'merge':
        try:
            success = merge_files(args.parts, args.output)
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == 'backup':
        try:
            import os
            if os.path.isdir(args.input):
                success = backup_directory(args.input, args.backup_dir,
                                           not args.no_timestamp)
            else:
                success = backup_file(args.input, args.backup_dir,
                                      not args.no_timestamp)
        except Exception as e:
            print(f"Error: {e}")

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
