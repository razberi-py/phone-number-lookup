# 📱 Phone Lookup Tool

> Advanced Phone Intelligence & OSINT Multi-Tool for comprehensive phone number analysis

**Made by:** razberi/xspoit

## 🚀 Quick Start

### Prerequisites

Make sure you have Python 3.6+ installed on your system.

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
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

## 🎯 Key Features

- **🔍 Deep Analysis**: 50+ comprehensive data points
- **🌐 Global Support**: Works with international phone numbers
- **📍 Location Intelligence**: Geographic and timezone information
- **⚡ Instant Results**: Fast offline processing
- **🛡️ Risk Assessment**: Built-in security evaluation
- **📊 Confidence Scoring**: Reliability metrics for each analysis
- **🎨 Beautiful Output**: Color-coded, organized results

## 📋 Output Categories

Results are organized into clear sections:

1. **📞 NUMBER_FORMATS** - All format variations
2. **✅ VALIDATION** - Validity and compliance checks
3. **🏗️ STRUCTURE** - Technical number breakdown
4. **🌍 GEOGRAPHIC_INFO** - Location and regional data
5. **🕐 TIMEZONE_INFO** - Time zone information
6. **📡 SERVICE_INFO** - Carrier and service details
7. **🔧 TECHNICAL_DATA** - Metadata and specifications
8. **📊 ANALYSIS** - Risk assessment and confidence scoring

## 🔒 Privacy & Security

- **Offline Processing**: No data sent to external servers
- **No Storage**: Numbers are not saved or logged
- **Risk Assessment**: Built-in security evaluation
- **Local Analysis**: All processing happens on your machine

## 🆘 Troubleshooting

### Common Issues

**"Invalid input" error:**
- Make sure to include the country code
- Use proper formatting (e.g., +1 for US numbers)
- Check for typos in the number

**Missing dependencies:**
```bash
pip install phonenumbers pytz pycountry
```

**Python version issues:**
- Requires Python 3.6 or higher
- Check your version: `python --version`

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

---

**⭐ If you find this tool useful, please give it a star!**

*Made with ❤️ by razberi/xspoit*
