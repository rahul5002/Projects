#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main() 
{
    int date, month, year, current_date, current_month, current_year, dayNumber = 0, current_day_no = 0;
    char Current_day[11];
    char current_day[11];

    printf("Enter the checking date:");
    scanf("%d", &date);
    printf("Enter the checking month:");
    scanf("%d", &month);
    printf("Enter the checking year:");
    scanf("%d", &year);
    printf("Enter the current date:");
    scanf("%d", &current_date);
    printf("Enter the current month:");
    scanf("%d", &current_month);
    printf("Enter the current year:");
    scanf("%d", &current_year);
    printf("Enter today's day:");
    scanf(" %s", Current_day);
    
   for (int i = 0; i < strlen(Current_day); i++) 
    {
        current_day[i] = tolower(Current_day[i]);
    }
    current_day[strlen(Current_day)] = '\0'; 
    

    if (strcmp(current_day, "sunday") == 0) dayNumber = 1;
    else if (strcmp(current_day, "monday") == 0) dayNumber = 2;
    else if (strcmp(current_day, "tuesday") == 0) dayNumber = 3;
    else if (strcmp(current_day, "wednesday") == 0) dayNumber = 4;
    else if (strcmp(current_day, "thursday") == 0) dayNumber = 5;
    else if (strcmp(current_day, "friday") == 0) dayNumber = 6;
    else if (strcmp(current_day, "saturday") == 0) dayNumber = 7;

    if ((date >= 1 && date <= 31) && (current_date >= 1 && current_date <= 31) && 
        (month >= 1 && month <= 12) && (current_month >= 1 && current_month <= 12) && 
        (year >= 1000 && year <= 9999) && (current_year >= 1000 && current_year <= 9999)) 
        {
            if (((month == 4 || month == 6 || month == 9 || month == 11) && date > 30) ||
            ((current_month == 4 || current_month == 6 || current_month == 9 || current_month == 11) && 
            current_date > 30)) 
        {
            printf("Invalid input as this month has only 30 days, try again.");
            return 0;
        }

        // Check February dates considering leap years
        if ((month == 2 || current_month == 2)) 
        {
            if (((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0))) 
            { 
                if (date > 29 || current_date > 29) 
                {
                    printf("Invalid input as February in a leap year has only 29 days.");
                    return 0;
                }
            }
            else 
            {
                if (date > 28 || current_date > 28) 
                {
                    printf("Invalid input as February has only 28 days.");
                    return 0;
                }
            }
        }

        printf("Date is: %d / %d / %d", date, month, year);

        int leapYearCount = 0;

        for (int i = (current_year + 1); i <= year; i++)
         {
            if ((i % 4 == 0 && i % 100 != 0) || (i % 400 == 0)) 
            {
                leapYearCount++;
            }
         }

        int numOfYears = year - (current_year + 1);
        int numLeapYears = leapYearCount;
        int numNonLeapYears = numOfYears - leapYearCount;

        int daysLeap = numLeapYears * 366;
        int daysNonLeap = numNonLeapYears * 365;

        int daysThisYear = 0;
        int daysElapsed = 0; 
        switch (current_month - 1) 
        {
            case 1: daysElapsed = 31; break;
            case 2: daysElapsed = 31 + 28; break;
            case 3: daysElapsed = 31 + 28 + 31; break;
            case 4: daysElapsed = 31 + 28 + 31 + 30; break;
            case 5: daysElapsed = 31 + 28 + 31 + 30 + 31; break;
            case 6: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30; break;
            case 7: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31; break;
            case 8: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31; break;
            case 9: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
           case 10: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
           case 11: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
           case 12: daysElapsed = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31; break;
           default: daysElapsed = 0;
        }
        daysElapsed += current_date;
        daysThisYear = (365 + ((current_year % 4 == 0 && current_year % 100 != 0) || (current_year % 400 == 0))) - daysElapsed;

        int days = 0;
        switch (month - 1) 
        {
            case 1: days = 31; break;
            case 2: days = 31 + 28; break;
            case 3: days = 31 + 28 + 31; break;
            case 4: days = 31 + 28 + 31 + 30; break;
            case 5: days = 31 + 28 + 31 + 30 + 31; break;
            case 6: days = 31 + 28 + 31 + 30 + 31 + 30; break;
            case 7: days = 31 + 28 + 31 + 30 + 31 + 30 + 31; break;
            case 8: days = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31; break;
            case 9: days = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30; break;
            case 10: days = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31; break;
            case 11: days = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30; break;
            case 12: days = 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31 + 30 + 31; break;
        }
        if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0)) 
        {
            days++;
        }

        int totalDay = days + date + daysThisYear + daysLeap + daysNonLeap-1;
        printf("\nTotal days = %d\n", totalDay);
        int dayDecider = totalDay % 7;
        printf(" Days not making a week = %d\n", dayDecider);
        current_day_no = (dayNumber + dayDecider) % 7;

        switch (current_day_no) 
        {
            case 0: printf("%s",Current_day);break;
            case 1: printf("Sunday"); break;
            case 2: printf("Monday"); break;
            case 3: printf("Tuesday"); break;
            case 4: printf("Wednesday"); break;
            case 5: printf("Thursday"); break;
            case 6: printf("Friday"); break;
            case 7: printf("Saturday"); break;
        }
    } else 
    {
        printf("Invalid input, try again.");
    }
    return 0;
}