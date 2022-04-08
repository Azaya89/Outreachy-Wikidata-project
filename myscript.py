import pywikibot

site = pywikibot.Site('en', 'wikipedia')
repo = site.data_repository()

def get_my_page(my_page):
    """Prints content of a page."""
    text = my_page.get()
    my_page.text = text
    try:
        print(text)
    except:
        print("This page does not exist!")

def get_page(Qid):
    """Returns article information from the wikidata site."""
    #Qid represents the Q identifier of the article in a string format.
    return  pywikibot.ItemPage(repo, Qid)

def edit_article(page, addtext= "Hello"):
    """Add text to the end of an article. Default text is 'Hello'."""
    text = page.get()
    text = text + "\n" + addtext
    page.text = text
    try:
        print(text)
        page.save("Saving test edit")
        return 1
    except:
        print("That didn't work!")
        return 0

def get_claims(page_info, Pid, error):
    """Prints first/last names of author(s) of article."""
    #Pid represents the property code of the author item
    try:
        for claim in page_info['claims'][Pid]:
            instance_value = claim.getTarget()
            instance_page_info = instance_value.get()
            print('\t\t\t' + instance_page_info['labels']['en'])
            print('\t\tQ identifier: ' + instance_value.title() + '\n')
    except:
        print(error)

def get_qualifiers(claim, Pid, title):
    """Prints qualifier information of authors."""
    if Pid in claim.qualifiers:
        qualifier = claim.qualifiers[Pid]
        print('\t'+ title +': ' + qualifier[0].getTarget())


def print_article(wd_item):
    """Prints article information from the wikidata site."""
    item_code = wd_item.title()
    page_info = wd_item.get()

    #Print title and Q identifier of article.
    try:
        print('\nTitle of article: \n' + page_info['labels']['en'])
        print('\nQ identifier of article:\n \t' + item_code + '\n')
    except:
        print('Item Name: This item has no English label!' + '\n')

    #Print author information in article, if any.
    try:
        for claim in page_info['claims']['P50']:
            print('Author Information:')
            name_value = claim.getTarget()
            name_page_info = name_value.get()
            title = name_value.title()
            
            #Print name and Q identifier of author.
            print('\tName: ' + name_page_info['labels']['en'])
            print('\tQ identifier: ' + title + '\n')
            
            #Print author qualifiers.
            print('\tQualifiers:')
            get_qualifiers(claim, 'P1932', 'Stated as')
            get_qualifiers(claim, 'P1545', 'Series ordinal')
            
            #Print given name and family name of author
            print('\n\tName info:')
            name_page = pywikibot.ItemPage(repo, title)
            author_dict = name_page.get()
            print('\t\tGiven name:') 
            get_claims(author_dict, 'P735', '\t\t*No given name info*')
            print('\t\tFamily name:')
            get_claims(author_dict, 'P734', '\t\t*No family name info*')
            print('\n')

    except:
        pass
    try:
        #Print author information for Author name string, if any.
        for claim in page_info['claims']['P2093']:
            print('Author Name String:')
            name_string_value = claim.getTarget()
            print('\tName: ' + name_string_value)
            get_qualifiers(claim, 'P1545', 'Series ordinal')
            get_qualifiers(claim, 'P1932', 'Stated as')
            print('\n')
    except:
        pass

def print_all_articles(articles):
    """Prints all articles in Outreachy task 1."""
    for item in articles:
        article = get_page(item)
        print_article(article)

articles = ['Q22065412', 'Q56904246', 'Q37416828', 'Q51538190', 'Q37624826', 'Q83849164', 'Q37072655', 'Q37624969', 'Q37506078']
my_page = pywikibot.Page(repo, 'User:Azaya89/Outreachy 1')
article = get_page('Q4115189')
get_my_page(my_page)
edit_article(my_page)
print_article(article)
print_all_articles(articles)
