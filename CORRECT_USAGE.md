# Ashley Voice - Correct Usage Examples

## ✅ CORRECT WAYS TO USE

### Method 1: Use stdin (pipe text directly) ← EASIEST
```bash
echo "Hello, I'm Ashley." | kokoro-tts - --voice ashley_neuro -o ashley.wav
```

### Method 2: Create a text file first
```bash
# Create input file
echo "Hello, I'm Ashley." > input.txt

# Generate audio
kokoro-tts input.txt --voice ashley_neuro -o ashley.wav
```

### Method 3: Use streaming with stdin
```bash
echo "Testing the neuro vtuber voice." | kokoro-tts - --voice ashley_neuro --stream
```

---

## ❌ WHAT DOESN'T WORK

```bash
# ❌ WRONG - Kokoro tries to read "Hello" as a filename
kokoro-tts "Hello" --voice ashley_neuro

# ❌ WRONG - Text in quotes is treated as filename
kokoro-tts "This is text" --voice ashley_neuro
```

---

## 📋 QUICK TEST COMMANDS (Copy & Paste)

### Test 1: Generate audio file to disk
```bash
echo "Hello, I'm Ashley. Testing the voice." | kokoro-tts - --voice ashley_neuro -o test_ashley.wav
```

### Test 2: Stream audio (play while generating)
```bash
echo "This is a longer test sentence to verify streaming works correctly." | kokoro-tts - --voice ashley_neuro --stream
```

### Test 3: Multiple sentences
```bash
echo "Hello there. How are you today? I am Ashley, your neuro vtuber voice." | kokoro-tts - --voice ashley_neuro -o multi.wav
```

### Test 4: Different speed
```bash
echo "Speaking quickly." | kokoro-tts - --voice ashley_neuro --speed 1.3 -o fast.wav
```

---

## 🔄 PIPING VS FILES

### Via stdin (easiest):
```bash
echo "text here" | kokoro-tts - --voice ashley_neuro -o output.wav
#                                    ^ dash means stdin
```

### Via file (more control):
```bash
# Create file
cat > mytext.txt << EOF
This is a longer text.
It can span multiple lines.
The voice will read it all.
EOF

# Convert to audio
kokoro-tts mytext.txt --voice ashley_neuro -o output.wav
```

---

## 💡 COMMON PATTERNS

### Generate and listen immediately (Windows)
```bash
echo "Test text" | kokoro-tts - --voice ashley_neuro -o temp.wav && start temp.wav
```

### Generate multiple variants
```bash
echo "Test" | kokoro-tts - --voice ashley_neuro -o v1.wav
echo "Test" | kokoro-tts - --voice af_sarah -o v2.wav
echo "Test" | kokoro-tts - --voice af_bella -o v3.wav
```

### Process entire book
```bash
kokoro-tts book.txt --voice ashley_neuro --split-output ./audiobook
```

---

## ✅ EXPECTED OUTPUT

When you run (for example):
```bash
echo "Hello Ashley" | kokoro-tts - --voice ashley_neuro -o test.wav
```

You should see:
```
✓ Processing output...
✓ Audio saved to: test.wav
```

Then a file `test.wav` appears in your current directory.

---

## 🎵 VERIFY IT WORKS

After generating:
```bash
# List file
dir test.wav

# Play it (Windows)
start test.wav
```

You should hear: **High-pitched, warm, clear female voice**

---

## QUICK FIX FOR YOUR ERROR

Your command:
```bash
kokoro-tts "Hello" --voice ashley_neuro
```

**Change to:**
```bash
echo "Hello" | kokoro-tts - --voice ashley_neuro
```

Or:
```bash
echo "Hello" > input.txt
kokoro-tts input.txt --voice ashley_neuro
```

That's it! Try one of these and it will work. 🚀
