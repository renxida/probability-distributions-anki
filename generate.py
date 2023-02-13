#%%


import genanki

# %%

#%%

import bs4
import requests
#%%

urls = [
    "https://en.wikipedia.org/wiki/Bernoulli_distribution",
    "https://en.wikipedia.org/wiki/Binomial_distribution",
    "https://en.wikipedia.org/wiki/Geometric_distribution",
    "https://en.wikipedia.org/wiki/Poisson_distribution",
    "https://en.wikipedia.org/wiki/Continuous_uniform_distribution",
    "https://en.wikipedia.org/wiki/Normal_distribution",
    "https://en.wikipedia.org/wiki/Exponential_distribution",
    "https://en.wikipedia.org/wiki/Gamma_distribution",
    "https://en.wikipedia.org/wiki/Beta_distribution",
    "https://en.wikipedia.org/wiki/Chi-squared_distribution",

]
#%%
url = urls[3]
soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")

print()

# %%
# <th scope="row" class="infobox-label"><a href="/wiki/Statistical_parameter" title="Statistical parameter">Parameters</a></th>

def get_data(url):

    soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")
    
    labels = soup.find_all("th", class_="infobox-label")
    data = soup.find_all("td", class_="infobox-data")

    # make dictionary from label to data
    data_dict = {}
    for i in range(len(labels)):
        label = labels[i].text
        data_dict[label] = "".join([str(x) for x in data[i].contents]).strip()
    
    # Name
    data_dict["Name"] = soup.find_all("span", class_="mw-page-title-main")[0].text
    # Explanation 
    first_p = soup\
        .find("table", class_="ib-prob-dist")\
        .find_next_sibling("p")
    data_dict["Explanation"] = first_p.text.split(".", 1)[0].strip()
    return data_dict
# %%
data_list = []
for url in urls:
    data = get_data(url)
    data_list.append(data)


# %%
data_list
# %%
ks = set()
for data in data_list:
    for k in data.keys():
        ks.add(k)

import collections
kc = collections.Counter()
for data in data_list:
    for k in data.keys():
        kc[k] += 1


# %%
ks
# %%

# Counter({'Parameters': 10,
#          'Support': 10,
#          'PMF': 4,
#          'CDF': 10,
#          'Mean': 10,
#          'Median': 10,
#          'Mode': 10,
#          'Variance': 10,
#          'MAD': 3,
#          'Skewness': 10,
#          'Ex. kurtosis': 10,
#          'Entropy': 10,
#          'MGF': 10,
#          'CF': 10,
#          'PGF': 4,
#          'Fisher information': 7,
#          'Name': 10,
#          'Notation': 6,
#          'PDF': 6,
#          'Quantile': 2,
#          'Kullback-Leibler divergence': 2,
#          'Method of Moments': 2})

my_model = genanki.Model(
  1320829343,
  'Probability Distribution',
  fields=[
    {'name': k} for k in ks
  ],
  templates=[
    {
      'name': 'Name2Mean',
      'qfmt': 'What is the mean of a {{Name}}?',
      'afmt': '{{FrontSide}}<hr id="answer">{{Mean}}',
    },
    {
      'name': 'Name2Parameters',
      'qfmt': 'What are the parameters of a {{Name}}?',
      'afmt': '{{FrontSide}}<hr id="answer">{{Parameters}}',
    },
    {
      'name': 'Name2Variance',
        'qfmt': 'What is the variance of a {{Name}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{Variance}}',
    },
    {
        'name': 'Name2CDF',
        'qfmt': 'What is the CDF of a {{Name}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{CDF}}',
    },
    {
        'name': 'Name2PMF',
        'qfmt': 'What is the PMF of a {{Name}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{PMF}}',
    },
    {
        'name': 'Name2PDF',
        'qfmt': 'What is the PDF of a {{Name}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{PDF}}',
    },
    {
        'name': 'PMF2Name',
        'qfmt': 'What is the name of the distribution with PMF {{PMF}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{Name}}',
    },
    {
        'name': 'CDF2Name',
        'qfmt': 'What is the name of the distribution with CDF {{CDF}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{Name}}',
    },
    {
        'name': 'PDF2Name',
        'qfmt': 'What is the name of the distribution with PDF {{PDF}}?',
        'afmt': '{{FrontSide}}<hr id="answer">{{Name}}',
    },
    {
        'name': 'Name2Explanation',
        'qfmt': 'What does a {{Name}} model?',
        'afmt': '{{FrontSide}}<hr id="answer">{{Explanation}}',
    },
  ])


notes = [
    [data[k] if k in data else "" for k in ks] for data in data_list
]


# %%
my_deck = genanki.Deck(2035271820, "Cedar's Probability Distributions")

for note in notes:
    my_note = genanki.Note(
      model=my_model,
      fields=note)
    my_deck.add_note(my_note)
# %%
genanki.Package(my_deck).write_to_file('CedarsProbabilityDistributions.apkg')

print("Generation Successful. Import CedarsProbabilityDistributions.apkg into Anki.")