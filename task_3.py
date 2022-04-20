import pywikibot
from myscript import repo, get_page, print_article
from bs4 import BeautifulSoup as bs
from urllib import request


def get_ris_authors(url=str):
    """Loads and saves the citation RIS in the URL, and returns a list of the authors."""
    html = request.urlopen(url).read()
    soup = bs(html, "html.parser")
    element = soup.find(attrs={"data-track-action" : "download article citation"})
    authors = []

    # Get citation url from the href attribute of the citation download element
    if element:
        citation_url = element['href']
        # Define the local filename to save data in.
        citation_file = 'citation.ris'

        #Download ris and save locally
        request.urlretrieve(citation_url, citation_file)

        #Read each line in the citation RIS and print only the author information.
        with open(citation_file) as file:
            for line in file:
                if line.startswith('AU'):
                    author = line.rstrip().split(' - ')[1]
                    authors.append(author)
                    #print(author)
   
    else:
        print("Citation does not exist.")

    return authors


def handle_qualifiers(claim, pid=str, names=str, title=str):
    """Prints qualifier information of authors if available and adds it if unavailable."""
    if pid in claim.qualifiers:
        qualifier = claim.qualifiers[pid]
        print(f'\t {title}:  {qualifier[0].getTarget()}')
    else:
        qualifier = pywikibot.Claim(repo, pid)
        qualifier.setTarget(names)
        claim.addQualifier(qualifier, summary=u'Added {title}')
        print(f'\tSuccessfully added {title}.')
        print(f'\t{title}: {names}')


def confirm_name(name_value, authors):
    """Confirms that the name is the same in Wikidata and RIS."""
    split_name = name_value.split()
    split_name.insert(0, split_name.pop())
    split_name[0] = split_name[0] + ','
    changed_format = " ".join(split_name)
    if changed_format in authors:
        print(f'\t{changed_format}')


def matched_author_info(wd_item, url):
    """Matches up author info from both wikidata and RIS"""
    page_info = wd_item.get()
    authors = get_ris_authors(url)

    try:
        for claim in page_info['claims']['P50']:
            name_value = claim.getTarget()
            name_page_info = name_value.get()
            split_name = name_value.split()

            #Print names of authors.
            print('\nWikidata name:')
            print('\t' + name_page_info['labels']['en'])
            print('RIS name:')
            confirm_name(name_value, authors)
            #If author has only one name, add it as given name only.
            if len(split_name) == 1:
                author_given_name = split_name[0]
                handle_qualifiers(claim, 'P9687', author_given_name, 'Author given name')
            else:
                #Author given name is every name except the last name listed.
                author_given_name = ' '.join(split_name[:-1])
                #Author last name is last name listed.
                author_last_name = split_name[-1]
                handle_qualifiers(claim, 'P9687', author_given_name, 'Author given name')
                handle_qualifiers(claim, 'P9688', author_last_name,'Author last name')
            print('\n')

    except:
        pass        

    try:
        for claim in page_info['claims']['P2093']:
            name_value = claim.getTarget()
            split_name = name_value.split()
            
            #Print names of authors.
            print('\nWikidata Name:')
            print(f'\t{name_value}')
            print('RIS name:')
            confirm_name(name_value, authors)

            #If author has only one name, add it as given name only.
            if len(split_name) == 1:
                author_given_name = split_name[0]
                handle_qualifiers(claim, 'P9687', author_given_name, 'Author given name')
            else:
                #Author given name is every name except the last name listed.
                author_given_name = ' '.join(split_name[:-1])
                #Author last name is last name listed.
                author_last_name = split_name[-1]
                handle_qualifiers(claim, 'P9687', author_given_name, 'Author given name')
                handle_qualifiers(claim, 'P9688', author_last_name,'Author last name')
            print('\n')
    except:
        pass


url = 'https://www.nature.com/articles/nbt1070#citeas'
article = get_page('Q51538190')
matched_author_info(article, url)
print_article(article)
get_ris_authors(url)