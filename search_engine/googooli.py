def making_database():
    '''
    This function reads text files from a folder and creates a database of their contents.

    Parameters:
    None

    Returns:
    list: A list of lists, where each sublist represents a line of text in a file and contains the following elements:
        - filename (str): The name of the file where the line was found.
        - line number (int): The line number in the file.
        - text (str): The text of the line.
        - relevance score (int): A score indicating how relevant the line is to a search query (initially set to 0).
    '''
    import os
    folderpath = './data_set'
    files_list = os.listdir(folderpath)
    database = []
    for file in files_list :
        with open(f"{folderpath}//{file}", mode = 'r', encoding = 'utf-8') as current_file:
            line_counter = 0
            for line in current_file:
                line_counter +=1
                words = line.split()
                text = ''
                for word in words :
                    text += word+' '
                database +=[[file, line_counter, text, 0]]
    return(database)


def input_query(message='\nPlease enter your query:'):
    '''
    This function prompts the user to enter a search query and returns the query as a lowercase string.

    Parameters:
    message (str): An optional message to display before prompting the user for input. Default is "\nPlease enter your query:".

    Returns:
    str: The user's search query as a lowercase string.
    '''
    print(message)
    return(input().lower())


def advanced_search(words):
    '''
    This function creates a new search query from a list of words for an advanced search.

    Parameters:
    words (list): A list of strings representing the words to include in the new search query.

    Returns:
    str or int: A string representing the new search query, or 0 if the list contains only one word.
    '''
    words_counter = len(words)
    new_query = ''
    if words_counter > 1:
        for n in range(words_counter-1):
            new_query += words[n]+' '
        return new_query
    return 0
        
                    
def search(query, database):
    '''
    This function searches a database of text lines for a given query and returns the search results.

    Parameters:
    query (str): The search query to look for.
    database (list): A list of lists representing the contents of the text files to be searched.

    Returns:
    tuple: A tuple containing two elements:
        - results_counter (int): The number of matching lines found.
        - results_list (list): A list of lists representing the matching lines. Each sublist contains four elements:
            - filename (str): The name of the file where the line was found.
            - line number (int): The line number in the file.
            - text (str): The text of the line.
            - relevance score (int): A score indicating how relevant the line is to the search query.
    '''
    results_counter = 0
    results_list = []
    n = 0
    for line in database :
        text = database[n][2].lower()
        if text.find(query) != -1 :
            results_counter += 1
            results_list.append(database[n])
        n += 1
    if results_counter == 0 :
        query = advanced_search(query.split())
        if query == 0:
            print("Your query could not be found.\n"
                  "Please check your spelling and try again.")
            main(database)
        results_counter, results_list, query= search(query, database)
    return results_counter, results_list, query


def test_IndexError(index, text):
    '''
    This function tests whether an index is valid for a given string and returns the index or the previous index if the index is out of range.

    Parameters:
    index (int): The index to test.
    text (str): The string to test the index against.

    Returns:
    int: The original index if it is valid, or the previous index if it is out of range.
    '''
    try :
        if text[index] :
            return index
    except IndexError :
        return index-1
    

def sort_results(query, results_list):
    '''
        This function sorts the search results based on their relevance to the search query.

    Parameters:
    query (str): The search query.
    results_list (list): A list of lists representing the search results.

    Returns:
    list: A sorted list of lists representing the search results, where each sublist contains the following elements:
        - filename (str): The name of the file where the line was found.
        - line number (int): The line number in the file.
        - text (str): The text of the line.
        - relevance score (int): A score indicating how relevant the line is to the search query .
    '''
    n = 0
    while n < len(results_list):
        text = results_list[n][2].lower()
        index = text.find(query)
        p_index = index-1
        n_index = test_IndexError(index+len(query), text)
        if (p_index == -1 or not(text[p_index].isalnum())) and not(text[n_index].isalnum()):
            pass
        elif p_index == -1 or not(text[p_index].isalnum()):
            results_list[n][3] = 1
        elif not(text[n_index].isalnum()):
            results_list[n][3] = 2
        else :
            results_list[n][3] = 3
        n += 1
    return sorted(results_list, key=lambda x:x[3])


def print_result(result_number, result, query):
    '''
    This function prints a single search result to the console.

    Parameters:
    result_number (int): The number of the search result to print.
    result (list): A list containing the following elements:
        - filename (str): The name of the file where the line was found.
        - line number (int): The line number in the file.
        - text (str): The text of the line.
        - relevance score (int): A score indicating how relevant the line is to the search query.
    query (str): The search query.

    Returns:
    None
    '''
    import os
    os.system("")
    white = '\033[37m'
    green = '\033[32m'
    orange = '\033[33m'
    purple = '\033[35m'
    text = result[2]
    index = text.lower().find(query)
    p_index = index-1
    n_index = index+len(query)
    if result_number % 2 == 0 :
        print(f"\n{white}Result {result_number} >>",
              f"{orange}File name: {result[0]}\n",
              f"{orange}Line {result[1]}: ", end = '')
        if index == 0 :
            print(f"{purple}{result[2][0:n_index]}{orange}{result[2][n_index:]}", white)
        else :
            print(f"{orange}{result[2][0:index]}{purple}{result[2][index:n_index]}{orange}{result[2][n_index:]}",white)
    else :
        print(f"\n{white}Result {result_number} >>",
              f"{green}File name: {result[0]}\n",
              f"{green}Line {result[1]}: ", end = '')
        if index == 0 :
            print(f"{purple}{result[2][0:n_index]}{green}{result[2][n_index:]}", white)
        else :
            print(f"{green}{result[2][0:index]}{purple}{result[2][index:n_index]}{green}{result[2][n_index:]}", white)
    return


def show_results(search_time, results_counter, results_list, query, message = ''):
    '''
    This function displays the search results to the user.

    Parameters:
    search_time (float): The time it took to perform the search, in seconds.
    results_counter (int): The number of matching lines found.
    results_list (list): A list of lists representing the matching lines. Each sublist contains four elements:
        - filename (str): The name of the file where the line was found.
        - line number (int): The line number in the file.
        - text (str): The text of the line.
        - relevance score (int): A score indicating how relevant the line is to the search query.
    query (str): The search query.
    message (str): An optional message to display before showing the search results. Default is an empty string.

    Returns:
    None
    '''
    print(message)
    print(f"\n{results_counter} results found in %0.2f seconds.\n" %(search_time) )
    result_number = 0
    while result_number < results_counter :
        i = 0
        while i < 10 and result_number < results_counter:
            print_result(result_number+1, results_list[result_number], query)
            result_number += 1
            i += 1
        if result_number < results_counter :
            print("Do you want to see the next page? y/n")
            if input().lower() == 'y':
                continue
            else :
                 break
    return


def main(database = making_database()):
    '''
    This function is the main entry point of the program. It allows the user to enter a query and displays the search results.

     Parameters:
     database (list): A list containing the data to be searched.

     Returns:
     None
    '''
    import time    
    while True :
        query = input_query()
        while True :
            if len(query) < 1 :
                query = input_query("Your query is too short!\nPlease enter a longer query:")
            else :
                break
        start_time = time.time()
        resalts = search(query, database)
        end_time = time.time()
        search_time = end_time - start_time
        results_counter = resalts[0]
        message = ''
        if query != resalts[2]:
            message = "Your desired phrase was not found.\nBut the results were found close to this expression."
            query = resalts[2]
        results_list = sort_results(query, resalts[1])
        show_results(search_time, results_counter, results_list, query, message)
        #This function runs forever, if you get tired, close the window manually ☺

main()
