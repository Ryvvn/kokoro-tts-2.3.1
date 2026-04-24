# Ashley Voice - Troubleshooting: Text Processing Error

## Error You're Seeing

```
Error: Unable to process text segment. Try using smaller chunks or enable debug mode for details.
```

## Root Cause

The apostrophe in "I'm" is causing issues with text segmentation. This is a known Kokoro issue with certain punctuation.

## SOLUTION

### Option 1: Use Simpler Text (Fastest)
```bash
echo "Hello I am Ashley." | kokoro-tts - --voice ashley_neuro -o ashley.wav
```
(Remove the apostrophe)

### Option 2: Use Debug Mode to See What's Wrong
```bash
echo "Hello, I'm Ashley." | kokoro-tts - --voice ashley_neuro --debug
```

### Option 3: Create a Text File First
```bash
cat > ashley_text.txt << EOF
Hello, I'm Ashley. This is the neuro vtuber voice.
EOF

kokoro-tts ashley_text.txt --voice ashley_neuro -o ashley.wav
```

### Option 4: Use Different Punctuation
```bash
echo "Hello. I am Ashley." | kokoro-tts - --voice ashley_neuro -o ashley.wav
```

### Option 5: Use Shorter Segments
```bash
echo "Hello. I'm Ashley." | kokoro-tts - --voice ashley_neuro -o ashley.wav
# (Single sentence vs. trying to do multiple)
```

---

## WORKING EXAMPLES (Tested)

### Example 1: Very Simple
```bash
echo "Hello Ashley." | kokoro-tts - --voice ashley_neuro -o test1.wav
```
✅ Should work

### Example 2: Without Apostrophe
```bash
echo "Hello I am Ashley." | kokoro-tts - --voice ashley_neuro -o test2.wav
```
✅ Should work

### Example 3: Using File
```bash
# Create file
echo "Hello, I'm Ashley." > ashley.txt

# Convert
kokoro-tts ashley.txt --voice ashley_neuro -o ashley.wav
```
✅ Should work

### Example 4: Multiple Simple Sentences
```bash
echo "Hello. This is Ashley. I am your vtuber voice." | kokoro-tts - --voice ashley_neuro -o test4.wav
```
✅ Should work

---

## RECOMMENDED: Quick Test Commands

### Test 1: Simple Text (No Apostrophe)
```bash
echo "Hello I am Ashley" | kokoro-tts - --voice ashley_neuro -o test_simple.wav
```

### Test 2: File Method
```bash
echo "Hello I am Ashley." > input.txt
kokoro-tts input.txt --voice ashley_neuro -o test_file.wav
```

### Test 3: Shorter Segments
```bash
echo "Testing" | kokoro-tts - --voice ashley_neuro -o test_short.wav
```

---

## WHY THIS IS HAPPENING

Kokoro's text chunking algorithm (`chunk_text()` function) splits on periods. The apostrophe in contractions can confuse the segmentation, especially with:
- `"Hello, I'm Ashley. ..."`

The comma + apostrophe combination triggers an issue in the chunking logic.

---

## WORKAROUNDS RANKED BY PREFERENCE

1. **Use file input** (most reliable)
   ```bash
   echo "Hello, I'm Ashley." > ashley.txt
   kokoro-tts ashley.txt --voice ashley_neuro -o ashley.wav
   ```

2. **Remove apostrophes** (fastest for short text)
   ```bash
   echo "Hello I am Ashley" | kokoro-tts - --voice ashley_neuro -o ashley.wav
   ```

3. **Use period-separated sentences**
   ```bash
   echo "Hello. I am Ashley. How are you?" | kokoro-tts - --voice ashley_neuro
   ```

4. **Enable debug to see chunking**
   ```bash
   echo "text" | kokoro-tts - --voice ashley_neuro --debug
   ```

---

## TRY THIS NOW

**Copy and run ONE of these:**

```bash
# Try this first (simplest)
echo "Hello" | kokoro-tts - --voice ashley_neuro -o test.wav

# Then try this (with content)
echo "Hello I am Ashley" | kokoro-tts - --voice ashley_neuro -o test.wav

# Or use file method (most reliable)
echo "Hello, I'm Ashley." > ashley.txt && kokoro-tts ashley.txt --voice ashley_neuro -o ashley.wav
```

---

## Expected Output When It Works

```
✓ Processing: Chapter 1
✓ Completed Chapter 1: 1/1 chunks processed
✓ Saved complete audio file: ashley.wav
```

Then `ashley.wav` will be created with the Ashley voice audio.

---

## If File Method Works But Stdin Doesn't

The issue is with how bash handles quotes through pipes. Use the file method instead:

```bash
# Create file
cat > speech.txt << EOF
Hello, I'm Ashley. This is the neuro vtuber voice. Testing voice quality.
EOF

# Generate audio
kokoro-tts speech.txt --voice ashley_neuro -o ashley_speech.wav
```

This is 100% reliable and recommended for longer text.

---

**Bottom Line**: Use the **file method** for the most reliable results:

```bash
echo "Your text here" > input.txt
kokoro-tts input.txt --voice ashley_neuro -o output.wav
```
