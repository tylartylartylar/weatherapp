# utils/display.py
"""
Module for formatting and displaying weather data.
"""

def fahrenheit_from_celsius(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def get_avg_temp(temp_list):
    """Calculate average temperature."""
    return sum(temp_list) / len(temp_list)

def get_opinion(average_temp):
    """Get opinion about the temperature."""
    if average_temp >= 70 and average_temp <= 83:
        opinion = "The temperature is fanfuckingtastic"
    elif average_temp <= 70 and average_temp >= 55:
        opinion = "Eh.. Wear a sweater and go outside, nerd"
    elif average_temp <=55 and average_temp >= 40:
        opinion = "It's not fantastic, but it could be a lot colder."
    else:
        opinion = "Its either hotter than 83 or colder than 40. You could stay inside if you want"
    return opinion