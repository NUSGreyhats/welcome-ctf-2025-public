## Solution

1. binwalk the disk image to find normal Linux EXT FS and OpenSSL
2. either use the offset from binwalk or use grep to determine byte offset of the `Salted__` sequence
3. use dd to carve and extract the file from previous found offset to end
4. use the given passphrase in the `sus_email.txt` to decrypt the encrypted portion with openssl
5. extract the gzip file and find flag