#include <stdio.h>
#include <limits.h>
#include <math.h>
int income(int profession, int income_range[2]);
int goal();
int expenses();
int emergency();
int savings(int income, int total_expenses);

int main()
{
    int profession, user_income, user_goal, user_expenses, user_savings, time_required;
    double year, rate_of_return;
    char choice, achieving_goal[100];
    int income_range[2];
    printf("Select your profession:\n1.Job\n2.Small Businessman/Businesswoman\n3.Large Businessman/Businesswoman\n4.Self Employed\n5.Others\n");
    scanf("%d", &profession);
    income(profession, income_range);
    user_income = (income_range[0] + income_range[1]) / 2;
    printf("What is your goal:");
    scanf("%s", &achieving_goal);
    user_goal = goal();
    user_expenses = expenses() + emergency();
    user_savings = savings(user_income, user_expenses);

    if ((user_expenses >= user_income * 12) || (user_savings <= 0))
    {
        printf("Your expenses exceed your income or you are not saving enough.You need to adjust your expenses or increase your income to achieve your goals.");
        return 0;
    }
    else
    {
        float time_required_months = (float)user_goal / (user_savings / 12);
        float time_required_years = time_required_months / 12;

        printf("Your current monthly savings are: %d\n",user_savings/12);
        printf("Rough estimation of time required to achieve your goals is: %.2f years\n", time_required_years);
        printf("Do you want to achieve your goal before time(press 'y' if yes and 'n' if no):");
        getchar();
        scanf("%c", &choice);
        if (choice == 'n')
            return 0;
        else
        {
            int avg_income = (income_range[0] + income_range[1]) / 2;
            if (profession == 1)
            { // Job
                if (avg_income <= 30000)
                    printf("Take Low Risk: Focus on safety and stability (fixed deposits, bonds).\n");
                else if (avg_income <= 50000)
                    printf("Take Moderate Risk: Balanced approach (mutual funds, balanced funds).\n");
                else if (avg_income <= 100000)
                    printf("Take Moderate to high risk: Possible investment in equities and index funds.\n");
                else
                    printf("Take High risk: Can consider aggressive investment strategies, including stocks and sector-specific mutual funds.\n");
            }
            else if (profession == 2)
            { // Small Business
                if (avg_income <= 15000)
                    printf("Take Low risk: Focus on savings and low-risk options.\n");
                else if (avg_income <= 50000)
                    printf("Take Moderate risk: Some investment in mutual funds and equities may be suitable.\n");
                else if (avg_income <= 100000)
                    printf("Take Moderate to high risk: Consider diversifying into stocks or real estate.\n");
                else
                    printf("Take High risk: Can explore more aggressive investments like startups or higher-risk stocks.\n");
            }
            else if (profession == 3)
            { // Large Business
                if (avg_income <= 250000)
                    printf("Take Moderate risk: Consider a balanced portfolio with equities and fixed income.\n");
                else if (avg_income <= 500000)
                    printf("Take High risk: Ability to invest in stocks, real estate, and high-growth assets.\n");
                else if (avg_income <= 1000000)
                    printf("Take Very high risk: Significant investment in equities, venture capital, or private equity.\n");
                else
                    printf("Take Extremely high risk: Explore high-risk investments including derivatives and foreign markets.\n");
            }
            else if (profession == 4)
            { // Self-Employed
                if (avg_income <= 50000)
                    printf("Take Low to moderate risk: Consider a mix of savings and moderate-risk investments.\n");
                else if (avg_income <= 100000)
                    printf("Take Moderate risk: Possible investments in balanced mutual funds and stocks.\n");
                else
                    printf("Take High risk: Explore more aggressive investments in equities or real estate.\n");
            }
            else if (profession == 5)
            { // Others
                if (avg_income <= 25000)
                    printf("Take Low risk: Focus on safe investments.\n");
                else if (avg_income <= 50000)
                    printf("Take Moderate risk: Introduce moderate-risk investments into the portfolio.\n");
                else
                    printf("Take High risk: Can consider aggressive investments based on comfort with risk.\n");
            }
        }
    }
    return 0;
}
int income(int profession, int income_range[2])
{
    int range;
    printf("Select your income range (Monthly):\n");
    switch (profession)
    {
    case 1: // Job
        printf("1. Rs 16,000-30,000\n2. Rs 30,000-50,000\n3. Rs 50,000-1,00,000\n4. Rs 1,00,000-3,00,000\n");
        break;
    case 2: // Small Business
        printf("1. Rs 8,000-15,000\n2. Rs 15,000-50,000\n3. Rs 50,000-1,00,000\n4. Rs 1,00,000-2,00,000\n");
        break;
    case 3: // Large Business
        printf("1. Rs 1,00,000-2,50,000\n2. Rs 2,50,000-5,00,000\n3. Rs 5,00,000-10,00,000\n4. Rs 10,00,000+\n");
        break;
    case 4: // Self-Employed
        printf("1. Rs 25,000-50,000\n2. Rs 50,000-1,00,000\n3. Rs 1,00,000-4,00,000\n");
        break;
    case 5: // Others
        printf("1. Rs 8,000-25,000\n2. Rs 25,000-50,000\n3. Rs 50,000-2,50,000\n");
        break;
    default:
        printf("Invalid input. Try again.\n");
        return 0;
    }
    scanf("%d", &range);
    if (range == 1)
    {
        if (profession == 1)
        {
            income_range[0] = 16000;
            income_range[1] = 30000;
        }
        else if (profession == 2)
        {
            income_range[0] = 8000;
            income_range[1] = 15000;
        }
        else if (profession == 3)
        {
            income_range[0] = 100000;
            income_range[1] = 250000;
        }
        else if (profession == 4)
        {
            income_range[0] = 25000;
            income_range[1] = 50000;
        }
        else if (profession == 5)
        {
            income_range[0] = 8000;
            income_range[1] = 25000;
        }
        else
            printf("Invalid input.Try again.\n");
    }
    else if (range == 2)
    {
        if (profession == 1)
        {
            income_range[0] = 30000;
            income_range[1] = 50000;
        }
        else if (profession == 2)
        {
            income_range[0] = 15000;
            income_range[1] = 50000;
        }
        else if (profession == 3)
        {
            income_range[0] = 250000;
            income_range[1] = 500000;
        }
        else if (profession == 4)
        {
            income_range[0] = 50000;
            income_range[1] = 100000;
        }
        else if (profession == 5)
        {
            income_range[0] = 25000;
            income_range[1] = 50000;
        }
        else
            printf("Invalid input.Try again.\n");
    }
    else if (range == 3)
    {
        if (profession == 1)
        {
            income_range[0] = 50000;
            income_range[1] = 100000;
        }
        else if (profession == 2)
        {
            income_range[0] = 50000;
            income_range[1] = 100000;
        }
        else if (profession == 3)
        {
            income_range[0] = 500000;
            income_range[1] = 1000000;
        }
        else if (profession == 4)
        {
            income_range[0] = 100000;
            income_range[1] = 400000;
        }
        else if (profession == 5)
        {
            income_range[0] = 50000;
            income_range[1] = 250000;
        }
        else
            printf("Invalid input.Try again.\n");
    }
    else if (range == 4)
    {
        if (profession == 1)
        {
            income_range[0] = 100000;
            income_range[1] = 300000;
        }
        else if (profession == 2)
        {
            income_range[0] = 100000;
            income_range[1] = 200000;
        }
        else if (profession == 3)
        {
            income_range[0] = 1000000;
            income_range[1] = INT_MAX;
        }
        else
            printf("Invalid input.Try again.\n");
    }
    else
    {
        printf("Invalid input. Try again.\n");
        return 0;
    }

    return 1;
}
int goal()
{
    long long int dream_worth;
    printf("Enter the approximate amount to reach your goal:\n");
    scanf("%lld", &dream_worth);
    return dream_worth;
}

int expenses()
{
    int monthly_expenses;
    printf("Enter your monthly expenses:\n");
    scanf("%d", &monthly_expenses);
    return monthly_expenses * 12;
}
int emergency()
{
    int emergency_expenses;
    printf("Enter your total emergency expense (if spent):\n");
    scanf("%d", &emergency_expenses);
    return emergency_expenses;
}
int savings(int income, int total_expenses)
{
    int yearly_income = income * 12;
    int saving = yearly_income - total_expenses;
    return saving;
}
