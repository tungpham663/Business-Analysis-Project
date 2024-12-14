from datetime import datetime

def calculate_months_difference(date_input):
    """
    Calculate the number of months between the earliest input date and today.

    Parameters:
        date_input (str): A date string in one of the formats: 
                          'DD/MM/YYYY', 'MM/YYYY', 'YYYY', or 'YYYY-YYYY'.
        
    Returns:
        int: Number of months difference (absolute value).
    """
    # Get today's date
    today = datetime.today()
    
    try:
            
        # Parse the input date based on its format
        if len(date_input.split("/")) == 3:  # DD/MM/YYYY
            input_date = datetime.strptime(date_input, "%d/%m/%Y")
        elif len(date_input.split("/")) == 2:  # MM/YYYY
            input_date = datetime.strptime(date_input, "%m/%Y")
        elif len(date_input.split("/")) == 1:  # YYYY
            input_date = datetime.strptime(date_input, "%Y")
        else:
            raise ValueError("Invalid date format.")
    
        # Calculate the number of months difference
        months_difference = (today.year - input_date.year) * 12 + (today.month - input_date.month)
        
        # Adjust for days if input_date has a day field
        if hasattr(input_date, 'day') and input_date.day > today.day and len(date_input.split("/")) == 3:
            months_difference -= 1
        
        return abs(months_difference)

    except ValueError as e:
        return f"Error: {str(e)}"