#include <stdio.h>
#include<string.h>
int main()
{
    int Book_ID[100], borrowed[100];
    char author[100][100], title[100][100];
    int total_books = 0;
    int student_id[100], borrowed_Book_ID[100];
    int total_borrowed = 0;
    int choice, i, found, book_id, stu_id, days_late, fine;

    while (1) 
    {
        printf("\nLibrary Management System\n");
        printf("1. Add Book\n");
        printf("2. Borrow Book\n");
        printf("3. Return Book\n");
        printf("4. Generate Reports\n");
        printf("5. Exit\n");
        printf("Enter your choice:\n");
        scanf("%d", &choice);

        switch (choice) 
        {
            case 1: // Add a new book
                if (total_books >= 100) 
                {
                    printf("Library is full. Cannot add more books.\n");
                    break;
                }
                printf("Enter Book ID: ");
                scanf("%d", &Book_ID[total_books]);
                printf("Enter title: ");
                scanf(" %[^\n]s", title[total_books]);
                printf("Enter author: ");
                scanf(" %[^\n]s", author[total_books]);
                borrowed[total_books] = 0;
                total_books++;
                printf("Book added successfully.\n");
                break;
            
            case 2: // Borrow a book
                printf("Enter Student ID: ");
                scanf("%d", &stu_id);
                printf("Enter Book ID: ");
                scanf("%d", &book_id);
                found = 0;
                for (i = 0; i < total_books; i++) 
                {
                    if (Book_ID[i] == book_id && borrowed[i] == 0) 
                    {
                        borrowed[i] = 1;
                        student_id[total_borrowed] = stu_id;
                        borrowed_Book_ID[total_borrowed] = book_id;
                        total_borrowed++;
                        printf("Book borrowed successfully by Student %d.\n", stu_id);
                        found = 1;
                        break;
                    }
                }
                if (!found) 
                {
                    printf("Book is either unavailable or already borrowed.\n");
                }
                break;

            case 3: // Return a book
                printf("Enter Student ID: ");
                scanf("%d", &stu_id);
                printf("Enter Book ID: ");
                scanf("%d", &book_id);
                printf("Enter number of days late: ");
                scanf("%d", &days_late);
                found = 0;
                fine = 0;
                for (i = 0; i < total_books; i++) 
                {
                    if (Book_ID[i] == book_id && borrowed[i] == 1) 
                    {
                        borrowed[i] = 0;
                        if (days_late > 0) {
                            fine = days_late * 10;
                            printf("Fine of Rs. %d Applied.\n", fine);
                        }
                        printf("Book returned successfully.\n");
                        found = 1;
                        break;
                    }
                }
                if (!found) {
                    printf("Book was not borrowed or wrong Book ID provided.\n");
                }
                break;

            case 4: // Generate reports
                printf("List of all available books:\n");
                for (i = 0; i < total_books; i++) {
                    if (borrowed[i] == 0) {
                        printf("Book ID: %d, Title: %s, Author: %s\n", Book_ID[i], title[i], author[i]);
                    }
                }
                printf("\nList of Borrowed Books:\n");
                for (i = 0; i < total_borrowed; i++) 
                {
                    for (int j = 0; j < total_books; j++) 
                    {
                        if (borrowed_Book_ID[i] == Book_ID[j]) 
                        {
                            printf("Student ID: %d, Borrowed Book ID: %d (Title: %s)\n", student_id[i], Book_ID[j], title[j]);
                            break;
                        }
                    }
                }
                break;

            case 5:
                return 0;

            default:
                printf("Invalid choice. Try again.\n");
        }
    }
    return 0;
}