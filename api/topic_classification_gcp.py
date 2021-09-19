from google.cloud import language_v1

def topic_classify(text, verbose=True):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={'document': document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print(u"=" * 20)
            print(u"{:<16}: {}".format("category", category.name))
            print(u"{:<16}: {}".format("confidence", category.confidence))

    return result

# takes {category1: category1_confidence, category2: categeory2_confidence ...} as input
# returns top k topics
# %%

def topic_dict_to_list(topics, k):
    res = []
    for key, value in topics.items():
        for topic in key.split("/")[1:]:
            if topic not in res:
                res.append(topic)
    return res[:k]
# %%
text = """
World War II or the Second World War, often abbreviated as WWII or WW2, was a 
global war that lasted from 1939 to 1945. It involved the vast majority of the 
world's countries—including all of the great powers—forming two opposing military 
alliances: the Allies and the Axis powers. In a total war directly involving more 
than 100 million personnel from more than 30 countries, the major participants 
threw their entire economic, industrial, and scientific capabilities behind the 
war effort, blurring the distinction between civilian and military resources. 
Aircraft played a major role in the conflict, enabling the strategic bombing of 
population centres and the only two uses of nuclear weapons in war to this day.
 World War II was by far the deadliest conflict in human history; it resulted in 
 70 to 85 million fatalities, a majority being civilians. Tens of millions of people died due to genocides (including the Holocaust), starvation, massacres, and disease. In the wake of the Axis defeat, Germany and Japan were occupied, and war crimes tribunals were conducted against German and Japanese leaders.
"""
# %%
text = """
William Henry Gates III (born October 28, 1955) is an American business magnate, software developer, investor, author, and philanthropist. He is a co-founder of Microsoft Corporation, along with his late childhood friend Paul Allen.[3][4] During his career at Microsoft, Gates held the positions of chairman, chief executive officer (CEO), president and chief software architect, while also being the largest individual shareholder until May 2014.[5] He is considered one of the best known entrepreneurs of the microcomputer revolution of the 1970s and 1980s.

Gates was born and raised in Seattle, Washington. In 1975, he and Allen founded Microsoft in Albuquerque, New Mexico. It became the world's largest personal computer software company.[6][a] Gates led the company as chairman and CEO until stepping down as CEO in January 2000, succeeded by Steve Ballmer, but he remained 
chairman of the board of directors and became chief software architect.[9] During the late 1990s, he was criticized for his business tactics, which have been considered anti-competitive. This opinion has been upheld by numerous court rulings.[10] In June 2008, Gates transitioned to a part-time role at Microsoft and full-time
 work at the Bill & Melinda Gates Foundation, the private charitable foundation he and his then-wife, Melinda Gates, established in 2000.[11] He stepped down as chairman of the board of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella.[12] In March 2020, Gates left his board positions at Microsoft and Berkshire Hathaway to focus on his philanthropic efforts including climate change, global health and development, and education.[13]
"""
# %%
text = """
The development of instruments that extend the human
senses has gone hand in hand with the advance of science.
The discovery and early study of cells progressed with the invention of microscopes in 1590 and their re nement during
the 1600s. Cell walls were rst seen by Robert Hooke in 1665
as he looked through a microscope at dead cells from the
bark of an oak tree. But it took the wonderfully crafted lenses
of Antoni van Leeuwenhoek to visualize living cells. Imagine
Hooke s awe when he visited van Leeuwenhoek in 1674 and
the world of microorganisms what his host called very little animalcules was revealed to him
"""
# %%
text = """
A useful technique for studying cell structure and function is
cell fractionation, which takes cells apart and separates
major organelles and other subcellular structures from one another (Figure 6.4). The instrument used is the centrifuge,
which spins test tubes holding mixtures of disrupted cells at a
series of increasing speeds. At each speed, the resulting force
causes a fraction of the cell components to settle to the bottom
of the tube, forming a pellet. At lower speeds, the pellet consists of larger components, and higher speeds yield a pellet
with smaller components.
Cell fractionation enables researchers to prepare specific
cell components in bulk and identify their functions, a task
not usually possible with intact cells. For example, on one of
the cell fractions, biochemical tests showed the presence of
enzymes involved in cellular respiration, while electron
microscopy revealed large numbers of the organelles called
mitochondria. Together, these data helped biologists determine that mitochondria are the sites of cellular respiration.
Biochemistry and cytology thus complement each other in
correlating cell function with structure
"""
# %%
text = """
Draughts or checkers is a group of strategy board games for two players which involve diagonal moves of uniform game pieces and mandatory captures by jumping over opponent pieces. Draughts developed from alquerque.[1] The name 'draughts' derives from the verb to draw or to move,[2] whereas 'checkers' derives from the checkered board which the game is played on.

The most popular forms are English draughts, also called American checkers, played on an 8×8 checkerboard; Russian draughts, Turkish draughts both on an 8x8 board, and International draughts, played on a 10×10 board. There are many other variants played on 8×8 boards. Canadian checkers and Singaporean/Malaysian checkers (also locally known as dum) are played on a 12×12 board.

English draughts was weakly solved in 2007 by a team of Canadian computer scientists led by Jonathan Schaeffer. From the standard starting position, both players can guarantee a draw with perfect play.
"""
# %%
#import os
#for k, v in sorted(os.environ.items()):
#    print(k+':', v)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Bill\Research\Javascript\kg_network_frontend\api\keys\geometric-rock-326004-a29eda0e9372.json"
#print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
