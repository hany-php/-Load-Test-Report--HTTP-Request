# ApacheBench (ab) Binaries

This directory contains the ApacheBench binaries for different operating systems.

## Directory Structure

```
vendor/ab/
├── windows/
│   └── ab.exe      # Windows binary
├── linux/
│   └── ab          # Linux binary
├── macos/
│   └── ab          # macOS binary
└── README.md       # This file
```

## Obtaining the Binaries

### Windows

1. **Download Apache Lounge binaries** (recommended):
   - Go to: https://www.apachelounge.com/download/
   - Download the latest Apache httpd ZIP (e.g., `httpd-2.4.x-win64-VSxx.zip`)
   - Extract the ZIP file
   - Find `ab.exe` in the `bin/` directory
   - Copy `ab.exe` to `vendor/ab/windows/`

2. **Or use XAMPP**:
   - If you have XAMPP installed, find `ab.exe` in:
     `C:\xampp\apache\bin\ab.exe`
   - Copy it to `vendor/ab/windows/`

### Linux

1. **Extract from apache2-utils package**:
   ```bash
   # On Debian/Ubuntu
   apt-get download apache2-utils
   dpkg -x apache2-utils_*.deb extracted/
   cp extracted/usr/bin/ab vendor/ab/linux/
   chmod +x vendor/ab/linux/ab
   ```

2. **Or build from source**:
   ```bash
   # Download Apache httpd source
   wget https://downloads.apache.org/httpd/httpd-2.4.x.tar.gz
   tar -xzf httpd-2.4.x.tar.gz
   cd httpd-2.4.x
   ./configure
   make
   # Find ab in support/.libs/ab
   ```

### macOS

1. **If Apache is installed via Homebrew**:
   ```bash
   # Install httpd if not already installed
   brew install httpd
   
   # Find ab location
   which ab
   # Usually: /usr/local/bin/ab or /opt/homebrew/bin/ab
   
   # Copy to vendor
   cp $(which ab) vendor/ab/macos/
   ```

2. **Or from Xcode Command Line Tools** (if available):
   - The ab binary might be available at `/usr/sbin/ab`

## Important Notes

- Make sure the binaries are executable (Linux/macOS):
  ```bash
  chmod +x vendor/ab/linux/ab
  chmod +x vendor/ab/macos/ab
  ```

- For production distribution, ensure you comply with the Apache License 2.0 terms.
  See `LICENSES/Apache-2.0.txt` and `THIRD_PARTY_NOTICES.txt` in the project root.

## License

ApacheBench is part of the Apache HTTP Server project and is licensed under the Apache License 2.0.
