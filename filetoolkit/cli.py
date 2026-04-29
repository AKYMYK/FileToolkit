"""
Command-line interface for FileToolkit.
Provides subcommands: encrypt, decrypt, convert, rename, hash, split, merge, backup, fileinfo, clean.
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
from .fileinfo import generate_report, file_age_summary, total_size_of_directory
from .cleaner import remove_empty_dirs, delete_temp_files, delete_old_files, clean_by_extension

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

    # ---------- fileinfo ----------
    info_parser = subparsers.add_parser('fileinfo', help='Show file/directory information')
    info_sub = info_parser.add_subparsers(dest='info_command')
    info_report = info_sub.add_parser('report', help='Generate directory report')
    info_report.add_argument('--directory', required=True, help='Directory to analyze')
    info_age = info_sub.add_parser('age', help='Show file age details')
    info_age.add_argument('--file', required=True, help='File to inspect')

    # ---------- clean ----------
    clean_parser = subparsers.add_parser('clean', help='Clean up directories')
    clean_sub = clean_parser.add_subparsers(dest='clean_command')
    clean_empty = clean_sub.add_parser('empty-dirs', help='Remove empty directories')
    clean_empty.add_argument('--directory', required=True)
    clean_empty.add_argument('--execute', action='store_true', help='Actually delete (default dry-run)')
    clean_temp = clean_sub.add_parser('temp', help='Delete temporary files')
    clean_temp.add_argument('--directory', required=True)
    clean_temp.add_argument('--execute', action='store_true', help='Actually delete')
    clean_old = clean_sub.add_parser('old', help='Delete old files')
    clean_old.add_argument('--directory', required=True)
    clean_old.add_argument('--days', type=int, default=30, help='Age threshold in days')
    clean_old.add_argument('--execute', action='store_true', help='Actually delete')
    clean_ext = clean_sub.add_parser('ext', help='Delete files by extension')
    clean_ext.add_argument('--directory', required=True)
    clean_ext.add_argument('--extensions', nargs='+', required=True, help='Extensions to delete (e.g. .tmp .log)')
    clean_ext.add_argument('--execute', action='store_true', help='Actually delete')

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
            if os.path.isdir(args.input):
                success = backup_directory(args.input, args.backup_dir,
                                           not args.no_timestamp)
            else:
                success = backup_file(args.input, args.backup_dir,
                                      not args.no_timestamp)
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == 'fileinfo':
        try:
            if args.info_command == 'report':
                print(generate_report(args.directory))
                success = True
            elif args.info_command == 'age':
                info = file_age_summary(args.file)
                for k, v in info.items():
                    print(f"{k}: {v}")
                success = True
        except Exception as e:
            print(f"Error: {e}")
    elif args.command == 'clean':
        dry = not getattr(args, 'execute', False)
        try:
            if args.clean_command == 'empty-dirs':
                removed = remove_empty_dirs(args.directory, dry_run=dry)
                action = "Would remove" if dry else "Removed"
                print(f"{action} {len(removed)} empty directories.")
                success = True
            elif args.clean_command == 'temp':
                deleted = delete_temp_files(args.directory, dry_run=dry)
                action = "Would delete" if dry else "Deleted"
                print(f"{action} {len(deleted)} temp files.")
                success = True
            elif args.clean_command == 'old':
                deleted = delete_old_files(args.directory, args.days, dry_run=dry)
                action = "Would delete" if dry else "Deleted"
                print(f"{action} {len(deleted)} old files (> {args.days} days).")
                success = True
            elif args.clean_command == 'ext':
                deleted = clean_by_extension(args.directory, args.extensions, dry_run=dry)
                action = "Would delete" if dry else "Deleted"
                print(f"{action} {len(deleted)} files with extensions {args.extensions}.")
                success = True
        except Exception as e:
            print(f"Error: {e}")

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
