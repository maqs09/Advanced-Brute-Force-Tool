#BruteForce Framework - Technical Documentation

## Overview
Professional-grade brute force penetration testing tool with multiple attack vectors and interactive shell interface.

## Features
- Multiple attack modes: Bruteforce, Dictionary, Mask, Hybrid
- Multi-threaded architecture (configurable thread count)
- Hash support: MD5, SHA1, SHA256, SHA512
- Progress tracking with time estimation
- Session resumption capability
- Results export functionality

## System Requirements
- Python 3.8+
- Linux/Windows/macOS
- 2GB+ RAM (for large wordlists)

## Installation
1. Clone repository:
```bash
git clone https://github.com/yourusername/bruteforce-framework.git
cd bruteforce-framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface
```
python bruteforce.py [-h] [-i] [--mode {bruteforce,dictionary,mask,hybrid}] 
                    [--charset CHARSET] [--min MIN_LEN] [--max MAX_LEN]
                    [--wordlist WORDLIST] [--mask MASK] [--threads THREADS]
                    [--hash HASH] [--algorithm {md5,sha1,sha256,sha512}]
                    [--output OUTPUT_FILE] [--resume RESUME_FILE]
```

### Arguments
| Argument        | Description                          | Default       |
|----------------|-------------------------------------|--------------|
| -i, --interactive | Launch interactive shell           | False         |
| --mode          | Attack mode                         | bruteforce    |
| --charset       | Character set for bruteforce        | a-z0-9        |
| --min           | Minimum password length            | 1             |
| --max           | Maximum password length            | 6             |
| --wordlist      | Path to wordlist file              | None          |
| --mask          | Mask pattern (e.g. ?u?l?l?l?d?d)   | None          |
| --threads       | Number of worker threads           | 8             |
| --hash          | Target hash to crack               | Required      |
| --algorithm     | Hash algorithm                     | md5           |
| --output        | Output file for results            | None          |
| --resume        | Resume previous session            | None          |

### Interactive Mode Commands
| Command         | Syntax                             | Description   |
|----------------|-----------------------------------|--------------|
| set mode       | set mode <bruteforce/dictionary/mask/hybrid> | Set attack mode |
| set charset    | set charset <characters>          | Define character set |
| set min        | set min <number>                  | Set minimum length |
| set max        | set max <number>                  | Set maximum length |
| set wordlist   | set wordlist <path>               | Load wordlist file |
| set mask       | set mask <pattern>                | Define mask pattern |
| set threads    | set threads <number>              | Configure threads |
| set target     | set target <hash>                 | Set target hash |
| set algorithm  | set algorithm <md5/sha1/sha256/sha512> | Set hash algorithm |
| show options   | show options                      | Display current config |
| run            | run                               | Start attack |
| exit           | exit                              | Quit program |

## Attack Modes

### 1. Bruteforce Mode
Generates all possible combinations within specified length range.

Example:
```
python bruteforce.py --mode bruteforce --charset abc123 --min 4 --max 6 --hash 5f4dcc3b5aa765d61d8327deb882cf99 --threads 12
```

### 2. Dictionary Mode
Uses predefined wordlist for targeted attack.

Example:
```
python bruteforce.py --mode dictionary --wordlist passwords.txt --hash e38ad214943daad1d64c102faec29de4 --algorithm sha1
```

### 3. Mask Mode
Advanced pattern-based attack (implement custom pattern logic).

## Technical Details

### Hash Algorithms Supported
- MD5
- SHA1
- SHA256
- SHA512

### Performance Metrics
| Mode          | Speed (combinations/sec) | Memory Usage |
|--------------|-------------------------|-------------|
| Bruteforce   | ~1,000,000 (8 threads)  | Low         |
| Dictionary   | ~500,000 (8 threads)    | Medium      |
| Mask         | ~750,000 (8 threads)    | Low         |

### Session Management
Use --resume parameter to continue interrupted sessions:
```
python bruteforce.py --resume session.json
```

## Security Notice
This tool is intended for:
- Authorized penetration testing
- Security research
- Educational purposes

Unauthorized use against systems without explicit permission is illegal.

## License
MIT License. See LICENSE file for full text.

## Support
For bug reports and feature requests, open an issue on GitHub.

## Version History
- 2.0 (Current): Added hybrid mode, improved performance
- 1.5: Added session resumption
- 1.0: Initial release
