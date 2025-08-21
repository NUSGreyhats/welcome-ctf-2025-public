# Welcome CTF 2025 Challenge List

### Welcome

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes | Sanity Check | Sanity check | 0 | 33000 |

### pwn

| Done? | Name                  | Challenge Details                              | Estimated Difficulty (1-5) | Port Number |
| ----- | --------------------- | ---------------------------------------------- | -------------------------- | ----------- |
| yes | python challenge | simple pyjail unicode bypass | 2 | 34508 |
| yes | machine code repl | write x64 shellcode to read file | 1 | 34568 |
| yes | blast from the past | buffer overflow and ret2shellcode | 2 | 35123 |
| yes | echocrash | negative indexing in BSS to overwrite GOT entry | 2.5 | 35124 |
| yes | Rusty Vending Machine | Integer underflow in Rust | 3 | TBC |
| yes | sunshinefactory | overwrite least significant byte of a function pointer to call win function | 4 | 33001 |


### Web

| Done? | Name         | Challenge Details                                      | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ------------------------------------------------------ | -------------------------- | ----------- |
| yes | ski buddy | JWT token bruteforce, WebSocket hijacking | 3 | 33335 |
| yes | goliath | Go JSON footguns | 2 | 3335 |
| yes | vibecoder | JWT Verify Bypass | 1 | 3334 |
| yes | This is just one of those classic web challenges | Simple but hopefully non-trivial SQLite injection | 2 | 33334 |
| yes | This is just another one of those classic web challenges | SVG XXS | 2 | 33333 |
| yes | secure file storage | zip upload symlink | 2 | 33336 |

### Crypto

| Done? | Name                     | Challenge Details                                                                                                       | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes | cat and xor scam | skip-ahead attack on xorshift cipher | 3 | - |
| yes | eccentric cryptographic cipher | Exploit RSA fixed points to factorize modulus | 2 | - |
| yes | baby feistel | derive all of feistel with given state | 1 | 32000 | 
| yes | what even is RSA | RSA with '2' as one of the primes | 0 | - |
| yes | please copy bthe ciphertext | simple XOR challenge | 1 | 31410 |

### RE

| Done? | Name         | Challenge Details                                      | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ------------------------------------------------------ | -------------------------- | ----------- |
| yes | mcshop | reverse a simple binary with extra steps to read flag file | 1 | 34612 |
| yes | flag checker | reverse a flag checker binary | 1 | - |
| yes | whats-in-the-bag | simple binary to re | 1 | - |
| yes | organised_person | custom packer to re | 2 | - |
| yes | wannaflag | self-extracting archive, re a binary + dll | 3 | - |
| yes | flag-checker-baby | reverse an (easier) flag checker binary | 2 | - |

### Forensics

| Done? | Name              | Challenge Details                                                                                                         | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes | shy zipper | b64 decode after EOCD of zipfile | 1 | - |
| yes | scrambled_pawtrait | xor the 2 images | 1 | - |
| yes | stolen_disk | openssl encrypted disk partition | 2.5 | - |
| yes | memory_exercise | volatile memory analysis | 1 | - |
| yes | cosmic bit flip | png file alpha channel disabled via metadata | 3 | - |
| yes | solved hangman | file signature and file metadata to extend png file | 2 | - |
| yes | baby_wireshark | Wireshark filter http traffic | 2 | - |
| yes | shapes_galore | microsoft macros function | 2 | - |

### Misc

| Done? | Name                    | Challenge Details                                                                               | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------------- | ----------------------------------------------------------------------------------------------- | -------------------------- | ----------- |
| yes | the next beethoven | pwntools automation | 1 | 34509 |
| yes | crazy gifarfe | Polyglot file (GIFAR, GIF + JAR) | 1 | - |
| yes | ADS | alternate data streams, circular bit shifting and audio visualising using a spectrogram | 1 | - |
| yes | What The Church | Searching for LLM Benchmark, Using HuggingFace | 2 | - |
| yes | NUS Geographer | use NUSMods venues.json, regex, map scripting | 4 | - |
| yes | BTS | Python zip iterator argument order weirdness | 2 | - |
| yes | Insanity Check | Whitespace Language encoding in Sanity Check's service | 2 | - |

### OSINT

| Done? | Name         | Challenge Details                                      | Estimated Difficulty (1-5) | Port Number |
| ----- | ------------ | ------------------------------------------------------ | -------------------------- | ----------- |
| yes | Someone's salty | Retrieve pre-migration post on mastodon | 1 | - |
| yes | Party in the USA | geoguesser ahh for greyhats sticker in LA | 1 | - |
| yes | i love greyhats | internet archive | 5 | - |

### Blockchain

| Done? | Name              | Challenge Details                                                                                                         | Estimated Difficulty (1-5) | Port Number |
| ----- | ----------------- | ------------------------------------------------------------------------------------------------------------------------- | -------------------------- | ----------- |


### README Templates

Essentially, all **README.md** files should contain the following information

| Things to include               | Example                                                                   |
| ------------------------------- | ------------------------------------------------------------------------- |
| Challenge Details               | `Caesar thought of the perfect cipher. Can you break it?`                 |
| Possible hints                  | `Hint: What Caesar Cipher?`                                               |
| Key concepts                    | `Scripting`                                                               |
| Solution (Can also be a script) | `Write a script to brute force all the combinations of the caesar cipher` |
| Learning objectives             | `Learn about the Caesar Cipher`                                           |
| Flag                            | `grey{salad_is_great_but_cipher_is_not}`                                  |

### Challenge folder format (challenges with services)
```
folder (your challenge name)
│   README.md
│   docker-compose.yml   
│
└───solve
│   │   (include all solution files here)
│
└───service
│   |   Dockerfile
│   |   (include all other files necessary for the service to run here e.g. .py files)
│      
└───distrib
    │   (include all files to be distributed to participants here)
```

### Challenge folder format (challenges without services)
```
folder (your challenge name)
│   README.md
│
└───solve
│   │   (include all solution files here)
│      
└───distrib
    │   (include all files to be distributed to participants here)
```
