#! /usr/bin/env python3

d = {
'అ':'a', 'ఆ':'ā', 'ఇ':'i', 'ఈ':'ī', 'ఉ':'u', 'ఊ':'ū', 'ఋ':'r̥',
'ౠ':'r̥̄', 'ఎ':'e', 'ఏ':'ē', 'ఐ':'ai', 'ఒ':'o', 'ఓ':'ō', 'ఔ':'au',

'ం':'ṁ', 'ఁ':'ă', 'ః':'ḥ', 

'క':'ka', 'ఖ':'kha', 'గ':'ga', 'ఘ':'gha', 'ఙ':'ṅa', 
'చ':'ca', 'ఛ':'cha', 'జ':'ja', 'ఝ':'jha', 'ఞ':'ña', 
'ట':'ṭa', 'ఠ':'ṭha', 'డ':'ḍa', 'ఢ':'ḍha', 'ణ':'ṇa', 
'త':'ta', 'థ':'tha', 'ద':'da', 'ధ':'dha', 'న':'na', 
'ప':'pa', 'ఫ':'pha', 'బ':'ba', 'భ':'bha', 'మ':'ma', 

'య':'ya', 'ర':'ra', 'ల':'la', 'వ':'va',  
'శ':'śa', 'ష':'ṣa', 'స':'sa', 'హ':'ha', 
'ఱ':'ṟa', 'ళ':'ḷa',  

'్':'+', 'ా':'+ā', 'ి':'+i', 'ీ':'+ī', 'ు':'+u', 'ూ':'+ū', 
'ృ':'+r̥',  'ౄ':'+r̥̄', 'ె':'+e', 'ే':'+ē', 'ై':'+ai', 
'ొ':'+o', 'ో':'+ō', 'ౌ':'+au', 

'"':'doublequote', "'":'singlequote', '?':'question', 
'(':'openparen', ')':'closeparen', '.':'dot'
}


def SmartD(key):
    try:
        return d[key]
    except KeyError:
        return key


def Map(s):
    if type(s) is list:
        return [Map(i) for i in s]
    elif type(s) is str:
        return ''.join([SmartD(i) for i in s]).replace('a+', '')
    else:
        raise TypeError


if __name__ == '__main__':
    భగ = '"నాఽయంలోకోఽస్తి న పరో న సుఖం సంశయాత్మనః?" - భగవద్గీత ౪,౪౦'
    అల్ల = ['అటజని','గాంచెఁ','భూమిసురుడంబర చుంబి','సురస్సరస్',]
    print(Map(భగ))
    print(Map(అల్ల))
