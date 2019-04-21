from django.core.exceptions import ValidationError 
from django.utils.translation import gettext_lazy as _  
    
def validate_time_error(startdate, duedate):
    if(duedate <= startdate): 
        raise ValidationError(
        'DueDate is earlier than StartDate !'
        ) 