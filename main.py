#!/usr/bin/env python3
"""
Advanced Offline Phone Intelligence
Author: Razberi Tech Innovations
Version: 2.0 - Enhanced with 50+ data points and location intelligence
"""

import sys
import json
import re
from datetime import datetime
import pytz
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, NumberParseException
from phonenumbers.phonemetadata import PhoneMetadata
from phonenumbers.phonenumberutil import (
    number_type, region_code_for_number,
    country_code_for_region, COUNTRY_CODE_TO_REGION_CODE,
    PhoneNumberType
)
import pycountry

def get_area_code_info(phone_number):
    """Extract and analyze area code information"""
    national_str = str(phone_number.national_number)
    area_code = None
    exchange_code = None
    subscriber_number = None
    
    # US/Canada NANP format analysis
    if phone_number.country_code == 1 and len(national_str) == 10:
        area_code = national_str[:3]
        exchange_code = national_str[3:6]
        subscriber_number = national_str[6:]
    elif len(national_str) >= 3:
        # For other countries, try to extract first 3-4 digits as area code
        area_code = national_str[:3] if len(national_str) >= 3 else None
        if len(national_str) >= 6:
            exchange_code = national_str[3:6]
            subscriber_number = national_str[6:]
    
    return {
        "area_code": area_code,
        "exchange_code": exchange_code,
        "subscriber_number": subscriber_number,
        "is_nanp_format": phone_number.country_code == 1 and len(national_str) == 10
    }

def get_enhanced_location_data(phone_number, region_code):
    """Get enhanced location information"""
    region_desc = geocoder.description_for_number(phone_number, "en")
    
    # Try multiple languages for region description
    region_desc_es = geocoder.description_for_number(phone_number, "es")
    region_desc_fr = geocoder.description_for_number(phone_number, "fr")
    
    # Analyze region description for more details
    location_parts = region_desc.split(",") if region_desc else []
    city = location_parts[0].strip() if location_parts else None
    state_province = location_parts[1].strip() if len(location_parts) > 1 else None
    
    return {
        "primary_location": region_desc,
        "location_spanish": region_desc_es if region_desc_es != region_desc else None,
        "location_french": region_desc_fr if region_desc_fr != region_desc else None,
        "city": city,
        "state_province": state_province,
        "location_confidence": "high" if region_desc and "," in region_desc else "medium" if region_desc else "low"
    }

def get_timezone_details(phone_number):
    """Get comprehensive timezone information"""
    tz_list = timezone.time_zones_for_number(phone_number)
    timezone_data = {
        "all_timezones": tz_list,
        "timezone_count": len(tz_list),
        "primary_timezone": tz_list[0] if tz_list else None,
        "spans_multiple_timezones": len(tz_list) > 1
    }
    
    if tz_list:
        primary_tz = pytz.timezone(tz_list[0])
        now = datetime.now(primary_tz)
        utc_now = datetime.utcnow()
        
        timezone_data.update({
            "local_time": now.isoformat(),
            "local_time_12h": now.strftime("%I:%M %p"),
            "local_date": now.strftime("%Y-%m-%d"),
            "utc_offset_hours": now.utcoffset().total_seconds() / 3600,
            "utc_offset_string": now.strftime("%z"),
            "is_dst": bool(now.dst()),
            "timezone_name": now.tzname(),
            "timezone_abbreviation": now.strftime("%Z")
        })
        
        # Add all timezone details if multiple
        if len(tz_list) > 1:
            all_tz_details = []
            for tz_name in tz_list:
                tz_obj = pytz.timezone(tz_name)
                tz_now = datetime.now(tz_obj)
                all_tz_details.append({
                    "timezone": tz_name,
                    "local_time": tz_now.isoformat(),
                    "utc_offset": tz_now.utcoffset().total_seconds() / 3600,
                    "abbreviation": tz_now.strftime("%Z")
                })
            timezone_data["all_timezone_details"] = all_tz_details
    
    return timezone_data

def enrich_phone(number_str: str) -> dict:
    try:
        # First try parsing without default region (for numbers with country code)
        pn = phonenumbers.parse(number_str, None)
    except NumberParseException:
        try:
            # If that fails, try with US as default region
            pn = phonenumbers.parse(number_str, "US")
        except NumberParseException as e:
            sys.exit(f"❌ Invalid input: {e}")

    # ═══════════════════════════════════════════════════════════════════════════
    # BASIC PHONE NUMBER INFORMATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    # Number Formats
    formats = {
        "input_number": number_str,
        "e164_format": phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164),
        "international_format": phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "national_format": phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL),
        "rfc3966_format": phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.RFC3966),
        "raw_input_cleaned": re.sub(r'[^0-9+]', '', number_str)
    }
    
    # Validation Status
    validation = {
        "is_valid_number": phonenumbers.is_valid_number(pn),
        "is_possible_number": phonenumbers.is_possible_number(pn),
        "is_valid_for_region": phonenumbers.is_valid_number_for_region(pn, region_code_for_number(pn)),
        "validation_result": "VALID" if phonenumbers.is_valid_number(pn) else "INVALID",
        "possible_length_local_only": str(phonenumbers.is_possible_number_with_reason(pn))
    }
    
    # Number Structure
    national_num = pn.national_number
    structure = {
        "country_code": pn.country_code,
        "national_number": national_num,
        "national_number_length": len(str(national_num)),
        "total_digits": len(re.sub(r'[^0-9]', '', formats["e164_format"])),
        "has_extension": hasattr(pn, 'extension') and pn.extension is not None,
        "extension": getattr(pn, 'extension', None),
        "has_italian_leading_zero": getattr(pn, "italian_leading_zero", False),
        "number_of_leading_zeros": getattr(pn, "number_of_leading_zeros", 0)
    }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # GEOGRAPHIC AND REGIONAL INFORMATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    reg_code = region_code_for_number(pn)
    country = pycountry.countries.get(alpha_2=reg_code) if reg_code else None
    
    geographic = {
        "region_code": reg_code,
        "country_name": country.name if country else None,
        "country_official_name": getattr(country, 'official_name', None) if country else None,
        "country_alpha_3": country.alpha_3 if country else None,
        "country_numeric_code": country.numeric if country else None,
        "associated_regions": COUNTRY_CODE_TO_REGION_CODE.get(pn.country_code, []),
        "region_count_for_country_code": len(COUNTRY_CODE_TO_REGION_CODE.get(pn.country_code, [])),
        "is_multi_region_country_code": len(COUNTRY_CODE_TO_REGION_CODE.get(pn.country_code, [])) > 1
    }
    
    # Enhanced Location Data
    location_data = get_enhanced_location_data(pn, reg_code)
    geographic.update(location_data)
    
    # Area Code Analysis
    area_info = get_area_code_info(pn)
    geographic.update(area_info)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # TIMEZONE AND TIME INFORMATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    timezone_info = get_timezone_details(pn)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CARRIER AND SERVICE INFORMATION
    # ═══════════════════════════════════════════════════════════════════════════
    
    carrier_name = carrier.name_for_number(pn, "en")
    num_type = number_type(pn)
    
    type_mapping = {
        PhoneNumberType.FIXED_LINE: "Fixed Line",
        PhoneNumberType.MOBILE: "Mobile",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line or Mobile",
        PhoneNumberType.VOIP: "VoIP",
        PhoneNumberType.TOLL_FREE: "Toll Free",
        PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        PhoneNumberType.SHARED_COST: "Shared Cost",
        PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        PhoneNumberType.PAGER: "Pager",
        PhoneNumberType.UAN: "Universal Access Number",
        PhoneNumberType.VOICEMAIL: "Voicemail",
        PhoneNumberType.UNKNOWN: "Unknown"
    }
    
    service_info = {
        "carrier_name": carrier_name,
        "carrier_available": bool(carrier_name),
        "number_type": type_mapping.get(num_type, "Unknown"),
        "number_type_code": str(num_type),
        "is_mobile": num_type == PhoneNumberType.MOBILE,
        "is_fixed_line": num_type == PhoneNumberType.FIXED_LINE,
        "is_fixed_or_mobile": num_type == PhoneNumberType.FIXED_LINE_OR_MOBILE,
        "is_voip": num_type == PhoneNumberType.VOIP,
        "is_toll_free": num_type == PhoneNumberType.TOLL_FREE,
        "is_premium_rate": num_type == PhoneNumberType.PREMIUM_RATE,
        "is_special_service": num_type in [PhoneNumberType.PREMIUM_RATE, PhoneNumberType.SHARED_COST, PhoneNumberType.UAN],
        "likely_billable": num_type not in [PhoneNumberType.TOLL_FREE, PhoneNumberType.VOICEMAIL]
    }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # DIALING AND TECHNICAL METADATA
    # ═══════════════════════════════════════════════════════════════════════════
    
    meta = PhoneMetadata.metadata_for_region(reg_code, None) if reg_code else None
    
    technical = {
        "national_prefix": getattr(meta, "national_prefix", None) if meta else None,
        "international_prefix": getattr(meta, "international_prefix", None) if meta else None,
        "national_prefix_for_parsing": getattr(meta, "national_prefix_for_parsing", None) if meta else None,
        "preferred_international_prefix": getattr(meta, "preferred_international_prefix", None) if meta else None,
        "national_prefix_optional_when_formatting": getattr(meta, "national_prefix_optional_when_formatting", False) if meta else False
    }
    
    # Example Numbers
    examples = {}
    for phone_type, type_name in [(PhoneNumberType.MOBILE, "mobile"), 
                                  (PhoneNumberType.FIXED_LINE, "fixed_line"),
                                  (PhoneNumberType.TOLL_FREE, "toll_free"),
                                  (PhoneNumberType.PREMIUM_RATE, "premium_rate")]:
        example_num = phonenumbers.example_number_for_type(reg_code, phone_type)
        if example_num:
            examples[f"example_{type_name}_number"] = phonenumbers.format_number(example_num, phonenumbers.PhoneNumberFormat.NATIONAL)
            examples[f"example_{type_name}_international"] = phonenumbers.format_number(example_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ANALYSIS AND METADATA
    # ═══════════════════════════════════════════════════════════════════════════
    
    analysis = {
        "lookup_timestamp_utc": datetime.utcnow().isoformat(),
        "lookup_timestamp_local": datetime.now().isoformat(),
        "data_sources": ["libphonenumber", "pycountry", "pytz"],
        "analysis_version": "2.0",
        "total_data_points": 0,  # Will be calculated
        "confidence_score": calculate_confidence_score(validation, geographic, service_info),
        "risk_assessment": assess_number_risk(num_type, geographic, validation)
    }
    
    # ═══════════════════════════════════════════════════════════════════════════
    # ASSEMBLE FINAL RESULT
    # ═══════════════════════════════════════════════════════════════════════════
    
    result = {
        "📱 NUMBER_FORMATS": formats,
        "✅ VALIDATION": validation,
        "🔢 STRUCTURE": structure,
        "🌍 GEOGRAPHIC_INFO": geographic,
        "🕐 TIMEZONE_INFO": timezone_info,
        "📡 SERVICE_INFO": service_info,
        "⚙️ TECHNICAL_DATA": technical,
        "📋 EXAMPLES": examples,
        "📊 ANALYSIS": analysis
    }
    
    # Calculate total data points
    total_points = sum(len(section) for section in result.values() if isinstance(section, dict))
    result["📊 ANALYSIS"]["total_data_points"] = total_points
    
    return result

def calculate_confidence_score(validation, geographic, service_info):
    """Calculate confidence score based on available data"""
    score = 0
    
    if validation["is_valid_number"]:
        score += 30
    if geographic["primary_location"]:
        score += 25
    if service_info["carrier_name"]:
        score += 20
    if geographic["area_code"]:
        score += 15
    if geographic["city"]:
        score += 10
    
    return min(score, 100)

def assess_number_risk(num_type, geographic, validation):
    """Assess potential risk factors of the number"""
    risk_factors = []
    risk_level = "LOW"
    
    if not validation["is_valid_number"]:
        risk_factors.append("Invalid number format")
        risk_level = "HIGH"
    
    if num_type == PhoneNumberType.PREMIUM_RATE:
        risk_factors.append("Premium rate number - charges may apply")
        risk_level = "MEDIUM"
    
    if num_type == PhoneNumberType.VOIP:
        risk_factors.append("VoIP number - location may not be accurate")
        if risk_level == "LOW":
            risk_level = "MEDIUM"
    
    if not geographic["primary_location"]:
        risk_factors.append("Location information unavailable")
    
    return {
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "is_safe_to_call": risk_level in ["LOW", "MEDIUM"] and validation["is_valid_number"]
    }

def format_output(result):
    """Format the output in a beautiful, organized way"""
    print("\n" + "═" * 80)
    print("📞 COMPREHENSIVE PHONE NUMBER ANALYSIS REPORT")
    print("═" * 80)
    
    # Display each section with nice formatting
    for section_name, section_data in result.items():
        if isinstance(section_data, dict):
            print(f"\n{section_name}")
            print("─" * len(section_name))
            
            for key, value in section_data.items():
                if value is not None:
                    if isinstance(value, bool):
                        value_str = "✅ Yes" if value else "❌ No"
                    elif isinstance(value, list) and value:
                        value_str = ", ".join(str(v) for v in value)
                    elif isinstance(value, dict):
                        value_str = json.dumps(value, indent=2)
                    else:
                        value_str = str(value)
                    
                    # Format key names to be more readable
                    formatted_key = key.replace("_", " ").title()
                    print(f"  {formatted_key:<30}: {value_str}")
    
    print("\n" + "═" * 80)
    print("🔍 Analysis Complete - Thank you for using Phone Intelligence!")
    print("═" * 80)

def main():
    # ANSI color codes for smooth purple gradient
    colors = {
        'light_purple': '\033[38;5;141m',    # Light purple
        'medium_purple': '\033[38;5;135m',   # Medium purple  
        'purple': '\033[38;5;129m',          # Standard purple
        'dark_purple': '\033[38;5;93m',      # Dark purple
        'deep_purple': '\033[38;5;57m',      # Deep purple
        'cyan': '\033[96m',
        'reset': '\033[0m',
        'bold': '\033[1m'
    }
    
    # ASCII Banner with smooth purple gradient
    banner = f"""{colors['bold']}
{colors['light_purple']}╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
{colors['medium_purple']}║{colors['light_purple']}★·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ {colors['medium_purple']}      ║
{colors['medium_purple']}║{colors['light_purple']}    ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗███████╗    ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗     {colors['medium_purple']}║
{colors['purple']}║{colors['medium_purple']}    ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔════╝    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗    {colors['purple']}║
{colors['purple']}║{colors['medium_purple']}    ██████╔╝███████║██║   ██║██╔██╗ ██║█████╗      ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝    {colors['purple']}║
{colors['dark_purple']}║{colors['purple']}    ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██╔══╝      ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝     {colors['dark_purple']}║
{colors['dark_purple']}║{colors['purple']}    ██║     ██║  ██║╚██████╔╝██║ ╚████║███████╗    ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║         {colors['dark_purple']}║
{colors['deep_purple']}║{colors['dark_purple']}    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝         {colors['deep_purple']}║
{colors['deep_purple']}║{colors['dark_purple']}★·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ ·.·´¯`·.·★ {colors['deep_purple']}      ║
{colors['deep_purple']}║{colors['dark_purple']}    {colors['cyan']}🔍 Advanced Phone Intelligence & OSINT Multi-Tool{colors['dark_purple']}                                                     ║
{colors['deep_purple']}║{colors['dark_purple']}    {colors['cyan']}📱 Deep Analysis • Location Tracking • Risk Assessment{colors['dark_purple']}                                                ║
{colors['deep_purple']}║{colors['dark_purple']}══════════════════════════════════════════════════════════════════════════════════════════════════════════{colors['deep_purple']}║
{colors['deep_purple']}║{colors['dark_purple']}    Made by: razberi/xspoit{colors['dark_purple']}                                                                               ║
{colors['deep_purple']}╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝{colors['reset']}
"""
    
    print(banner)
    
    # Get user input
    phone_number = input("\n📞 Enter phone number to analyze (with country code, e.g., +1234567890): ")
    
    if not phone_number.strip():
        print("\n❌ Error: No phone number provided.")
        sys.exit(1)
    
    print("\n🔄 Analyzing phone number...")
    print("   • Parsing number format")
    print("   • Validating number structure")
    print("   • Gathering geographic data")
    print("   • Retrieving carrier information")
    print("   • Calculating risk assessment")
    
    try:
        result = enrich_phone(phone_number.strip())
        
        # Display formatted results
        format_output(result)
        
        # Quick summary
        analysis = result.get("📊 ANALYSIS", {})
        validation = result.get("✅ VALIDATION", {})
        geographic = result.get("🌍 GEOGRAPHIC_INFO", {})
        
        print("\n" + "═" * 80)
        print("📋 QUICK SUMMARY")
        print("═" * 80)
        print(f"📊 Total Data Points: {analysis.get('total_data_points', 'N/A')}")
        print(f"✅ Number Valid: {'Yes' if validation.get('is_valid_number') else 'No'}")
        print(f"🌍 Location: {geographic.get('primary_location', 'Unknown')}")
        print(f"🏆 Confidence Score: {analysis.get('confidence_score', 0)}%")
        
        risk_info = analysis.get('risk_assessment', {})
        risk_level = risk_info.get('risk_level', 'UNKNOWN')
        risk_color = "🟢" if risk_level == "LOW" else "🟡" if risk_level == "MEDIUM" else "🔴"
        print(f"⚠️  Risk Level: {risk_color} {risk_level}")
        
        if risk_info.get('risk_factors'):
            print("⚠️  Risk Factors:")
            for factor in risk_info['risk_factors']:
                print(f"     • {factor}")
        
        print("\n" + "═" * 80)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
