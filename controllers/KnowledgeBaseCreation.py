import collections


# No Automated cleaning of output yet.

# Automated cleaning and JSON format output to follow

# This function creates and outputs the knowledge base into a text file.  This function just needs the list of ngrams

def createKnowledgeBase(ngramsList):
    known_names = ["Rodrigo", "Digong", "Du30", "Duterte", "Grace", "Poe", "Miriam", "Defensor", "Santiago", "Mar",
                   "Roxas", "Jejomar", "Binay"]

    found_names = collections.defaultdict(list)

    for name in known_names:

        for ngrams in ngramsList:

            if name.lower() in ngrams.lower():
                found_names[name].append(ngrams)

    # Write to text file - *Not yet in JSON Format*

    kb = open("KnowledgeBase.txt", "w")

    for key, value in found_names.items():
        kb.write('%s:%s\n' % (key, value))

    kb.close()
