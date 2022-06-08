import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def makesummary(text):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm') 
    doc = nlp(text) 
    tokens = [token.text for token in doc]
    punctuation='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\n'

    word_fq = {}
    for word in  doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_fq.keys():
                    word_fq[word.text] = 1
                else:
                    word_fq[word.text]+=1

                    
    max_fq = max(word_fq.values())
    for word in word_fq.keys():
            word_fq[word] = word_fq[word]/max_fq
            
            
    s_tokens = [sent for sent in doc.sents]

    s_score = {}
    for sent in s_tokens:
        for word in sent:
            if word.text.lower() in word_fq.keys():
                if sent not in s_score.keys():
                    s_score[sent]= word_fq[word.text.lower()]
                else:
                    s_score[sent]+= word_fq[word.text.lower()]
                    

    s_length = int(len(s_tokens)*0.5)
    summary = nlargest(s_length,s_score,key =s_score.get)
    f_sum = [word.text for word in summary]
    summary = " ".join(f_sum)
    print(summary)
    return len(summary)
    
x = ''' Real Madrid Club de Fútbol (Spanish pronunciation: [reˈal maˈðɾið ˈkluβ ðe ˈfuðβol] (audio speaker iconlisten), meaning Royal Madrid Football Club), commonly referred to as Real Madrid, is a Spanish professional football club based in Madrid.Founded on 6 March 1902 as Madrid Football Club, the club has traditionally worn a white home kit since inception. The honorific title real is Spanish for "royal" and was bestowed to the club by King Alfonso XIII in 1920 together with the royal crown in the emblem. The team has played its home matches in the 81,044-capacity Santiago Bernabéu Stadium in downtown Madrid since 1947. Unlike most European sporting entities, Real Madrid's members (socios) have owned and operated the club throughout its history.The club was estimated to be worth €3.8 billion ($4.2 billion) in 2019, and it was the second highest-earning football club in the world, with an annual revenue of €757.3 million in 2019.[6][7] The club is one of the most widely supported teams in the world.[8] Real Madrid is one of three founding members of La Liga that have never been relegated from the top division since its inception in 1929, along with Athletic Bilbao and Barcelona. The club holds many long-standing rivalries, most notably El Clásico with Barcelona and El Derbi Madrileño with Atlético Madrid.Real Madrid established itself as a major force in both Spanish and European football during the 1950s, winning five consecutive European Cups and reaching the final seven times. This success was replicated in the league, which the club won five times in the space of seven years. This team, which included Alfredo Di Stéfano, Ferenc Puskás, Francisco Gento, and Raymond Kopa, is considered by some in the sport to be the greatest team of all time.[9][10][11]In domestic football, the club has won 67 trophies; a record 34 La Liga titles, 19 Copa del Rey, 12 Supercopa de España, a Copa Eva Duarte, and a Copa de la Liga.[12] In European and worldwide competitions, Real Madrid have won a record 26 trophies; a record 13 European Cup/UEFA Champions League titles, two UEFA Cups and four UEFA Super Cups. In international football, they have achieved a record seven club world championships.[note 1]Real Madrid was recognised as the FIFA Club of the 20th Century on 11 December 2000 with 42.35% of the vote,[14] and received the FIFA Centennial Order of Merit on 20 May 2004.[15] The club was also awarded Best European Club of the 20th Century by the IFFHS on 11 May 2010. In June 2017, the team succeeded in becoming the first club to win consecutive Champions League titles, then made it three in a row and four in five seasons in May 2018, extending their lead atop the UEFA club rankings. As of 2020, Real Madrid are ranked third behind Bayern Munich and Barcelona'''
print("Original ","Length",len(x))
print(x)
print("SUMMARY START")
t = makesummary(x)
print("Summary ","Length",t)
