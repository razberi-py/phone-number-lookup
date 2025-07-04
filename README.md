# 📱 Phone Lookup Tool

> Advanced Phone Intelligence & OSINT Multi-Tool for comprehensive phone number analysis

**Made by:** razberi/xspoit

## 🚀 Quick Start

### Prerequisites

Make sure you have Python 3.6+ installed on your system.

### Installation

1. Clone this repository:
```bash
git clone <repo-url>
cd <repo-name>
```

2. Install required dependencies:
```bash
pip install phonenumbers pytz pycountry
```

### Usage

1. Run the tool:
```bash
python main.py
```

2. Enter a phone number when prompted:
   - Include country code (e.g., `+1234567890`)
   - Or use national format (e.g., `(555) 123-4567` for US numbers)

3. View the comprehensive analysis results!

## 📊 What You Get

The tool provides **50+ data points** organized into these categories:

### 📞 Number Formats
- E164 International Format
- National Format
- RFC3966 Format
- Raw Input Analysis

### ✅ Validation Status
- Number validity check
- Regional validation
- Possibility assessment
- Format compliance

### 🏗️ Number Structure
- Country code breakdown
- National number analysis
- Extension detection
- Digit count analysis

### 🌍 Geographic Information
- Country identification
- Region mapping
- Location details
- Area code analysis
- Multi-region detection

### 🕐 Timezone Data
- Primary timezone
- All possible timezones
- Current local time
- UTC offset information
- Timezone abbreviations

### 📡 Service Information
- Carrier identification
- Number type classification
- Service provider details
- Line type analysis

### 🔧 Technical Metadata
- Dialing patterns
- Example numbers
- Format specifications
- Regional metadata

### 📊 Analysis & Risk Assessment
- Confidence scoring
- Risk level evaluation
- Anomaly detection
- Quality assessment

## 💡 Usage Examples

### US Numbers
```
📞 Enter phone number: +1 (555) 123-4567
📞 Enter phone number: 555-123-4567
📞 Enter phone number: 15551234567
```

### International Numbers
```
📞 Enter phone number: +44 20 7946 0958
📞 Enter phone number: +33 1 42 86 83 26
📞 Enter phone number: +81 3-3570-4311
```

### Common Issues

**"Invalid input" error:**
- Make sure to include the country code
- Use proper formatting (e.g., +1 for US numbers)
- Check for typos in the number

*Made with ❤️ by razberi/xspoit*
