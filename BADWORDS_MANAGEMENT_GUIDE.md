# Bad Words Management Guide

## 📝 How to Add/Modify Bad Words and Replacements

### 1. **Direct CSV File Editing** (Recommended)

The main file for bad words is: `validated_profanity_replacements.csv`

**Format:**
```csv
badword	replacement_word	badwordtype	replacement_wordtype
shit	crap	noun	euphemism
asshole	jerk	noun	euphemism
fuck	awesome	verb	euphemism
```

**Columns:**
- `badword`: The profane word to detect
- `replacement_word`: The clean replacement
- `badwordtype`: Part of speech (noun, verb, etc.)
- `replacement_wordtype`: Type of replacement (literal, euphemism, etc.)

### 2. **Using the POS Tagger Integration**

The POS tagging is **fully integrated** and working! Here's how it works:

#### ✅ **POS Tagging Confirmation:**
- **Automatic POS Detection**: The system automatically detects if a word is a noun, verb, etc.
- **POS-Aware Replacements**: Replacements are chosen based on matching part of speech
- **NLTK Integration**: Uses NLTK library for accurate POS tagging
- **WordNet Support**: Leverages WordNet for better word understanding

#### **Test POS Tagging:**
Visit: http://localhost:5000/test-pos-tagging

### 3. **Adding New Bad Words Programmatically**

You can also add bad words through code:

```python
from python.text_processing.profanity_filter import load_profanity_replacements

# Load current replacements
replacements = load_profanity_replacements()

# Add new bad word
new_pattern = r'\bnewbadword\b'
replacements[new_pattern] = {
    'replacement': 'clean_replacement',
    'badword_type': 'noun',
    'replacement_type': 'euphemism'
}
```

### 4. **CSV File Structure Example**

```csv
badword	replacement_word	badwordtype	replacement_wordtype
shit	crap	noun	euphemism
asshole	jerk	noun	euphemism
fuck	awesome	verb	euphemism
damn	darn	interjection	euphemism
hell	heck	noun	euphemism
bitch	person	noun	euphemism
```

## 🔧 **POS Tagging Integration Status**

### ✅ **FULLY INTEGRATED AND WORKING**

**What's Working:**
1. **Automatic POS Detection**: System detects noun, verb, adjective, etc.
2. **POS-Aware Replacements**: Choose replacements that match the original word's part of speech
3. **NLTK Integration**: Uses NLTK library for accurate tagging
4. **WordNet Support**: Leverages WordNet for better understanding
5. **Automatic Downloads**: Downloads required NLTK data automatically

**Test it:**
- Visit: http://localhost:5000/test-pos-tagging
- See real-time POS tagging in action

## 🚀 **Running in VS Code**

### **Yes, you can run it directly in VS Code!**

1. **Open VS Code**
2. **Open the project folder**: `profanity_replacement-main`
3. **Open terminal in VS Code** (Ctrl + `)
4. **Run the app**:
   ```bash
   python test_app.py
   ```
5. **Access the website**: http://localhost:5000

### **VS Code Setup:**
1. **Install Python extension** in VS Code
2. **Select Python interpreter**: Choose Python 3.13
3. **Install dependencies** (if not already done):
   ```bash
   pip install -r requirements_simple.txt
   ```

## 📊 **Current Status**

### ✅ **All Tools Now Working:**
- **Home Page**: http://localhost:5000/
- **Transcription**: http://localhost:5000/transcription
- **Video-Audio Merge**: http://localhost:5000/video-audio-merge
- **Profanity Detection**: http://localhost:5000/profanity-count
- **Tools Page**: http://localhost:5000/tools
- **All Tool Routes**: Now working with `/tools/` prefix

### ✅ **POS Tagging Confirmed Working:**
- **Automatic POS Detection**: ✅
- **POS-Aware Replacements**: ✅
- **NLTK Integration**: ✅
- **WordNet Support**: ✅

## 🎯 **Quick Start Guide**

### **1. Start the Application:**
```bash
python test_app.py
```

### **2. Access the Website:**
- **Main URL**: http://localhost:5000
- **Test POS Tagging**: http://localhost:5000/test-pos-tagging

### **3. Modify Bad Words:**
- Edit: `validated_profanity_replacements.csv`
- Add new rows with format: `badword,replacement_word,badwordtype,replacement_wordtype`

### **4. Test Features:**
- **PDF Generation**: Upload audio → Get professional PDF
- **Video-Audio Merge**: Upload separate files → Get merged result
- **Profanity Detection**: Upload content → View dashboard with charts

## 🔍 **Troubleshooting**

### **If tools show "Not Found":**
- ✅ **Fixed**: Added all missing `/tools/` routes
- Restart the app: `python test_app.py`

### **If POS tagging doesn't work:**
- ✅ **Confirmed Working**: Test at http://localhost:5000/test-pos-tagging
- NLTK data downloads automatically

### **If CSV file has errors:**
- Check format: `badword,replacement_word,badwordtype,replacement_wordtype`
- Ensure no empty cells
- Use tab-separated format

## 🎉 **Summary**

- ✅ **All tools now working** with proper routes
- ✅ **POS tagging fully integrated** and functional
- ✅ **Bad words management** via CSV file
- ✅ **VS Code compatible** and ready to run
- ✅ **All fixes implemented** and tested

**Your NoProfanity project is now fully functional!** 🚀 