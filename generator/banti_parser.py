import re
from TeluguFontProperties import FP_DICT

vattu_havers = 'ఖఘఛఝటఢథధఫభ'
two_piecers = 'ఘపఫషసహ'
gho_style = None
repha_style = None
ppu_present = None

def set_params(font_name):
    global gho_style, repha_style, ppu_present
    for k, [SIZE, GHO, REPHA, PPU, SPACING, ABBR, BOLD] in FP_DICT.items():
        if ABBR == font_name:
            gho_style = GHO
            repha_style = REPHA
            ppu_present = PPU
            break
    else:
        print('Could not find properties for: ', font_name)
        raise KeyError(font_name)



def process_pain_letters(word):
    # Class of tick plus underlying consonant + vowel 
    if '''ఘాఘుఘూఘౌపుపూఫుఫూషుషూసుసూహా
    హుహూహొహోహౌ'''.find(word) >= 0:
        return ['✓', word]            

    # Class of vowel-mark + underlying consonant base
    if '''ఘిఘీఘెఘేపిపీపెపేఫిఫీఫెఫేషిషీషెషేసిసీసె
    సేహిహీహెహేఘ్ప్ఫ్ష్స్హ్ '''.find(word) >= 0:
        return [word[1], word[0]]        

    # Detached ai-karams
    if 'ఘైపైఫైషైసైహై'.find(word) >= 0:
        return ['ె' , word[0], 'ై']

    # gho
    if 'ఘొఘో'.find(word) >= 0:
        if gho_style == 'T':           # Telugu style ఘొఘో
            return ['✓', word]
        else:                           # Kannada style
            return ['ె', 'ఘా' if word == 'ఘో' else 'ఘు']

    # Combining marks like saa, pau etc.
    return [word]

def get_letters_from_line(line):
    words = re.split('\s+', line.rstrip())
    line_glps = []
    for word in words:
        glps = []

        # ఏ Special Case
        if word == 'ఏ':
            glps += ['ఏ', 'ఎ']
        
        # Punc, Single Letters
        elif len(word) == 1:                             
            if word in two_piecers: glps += ['✓']
            glps += [word]
        
        # Cons + Vowel
        elif len(word) == 2:  
            if word[0] in two_piecers:
                glps += process_pain_letters(word)
            elif word[1] in 'ఁంఃృౄై':
                glps += [word[0]+ ('ె' if word[1] == 'ై' else '')]
                glps += [word[1]]
            else:
                glps += [word]
        
        # ppu special case
        elif word == 'ప్పు':
            if ppu_present :  
                glps += ['✓', 'ప', '్పు']
            else:
                glps += ['✓', 'పు', '్ప']
        
        # Cons Joiner Cons Vowel
        elif len(word) == 4 and word[1] == '్':  
            glps += [word[0] + word[3]]
            glps += ['్' + word[2]]
            if word[2] == 'ర':
                if repha_style == 'R':
                    glps[-1] +=  'R'
                elif repha_style == 'L':        # Swap order and pray to God
                    glps[-1] = glps[-2]
                    glps[-2] = '్రL'
        
        # The Rest - including Cons Joiner Cons
        else:
            print("ERROR in recognizing ", word)
        
        line_glps += [glps]
    
    return line_glps

def contains_vattu_haver(word_texts):
    for c in vattu_havers:
        if c in ''.join(word_texts):
            return True
            break
    else:
        return False            

def vattu_haver_index(word_texts):
    for i in range(len(word_texts)):
        if contains_vattu_haver(word_texts[i]):
            return i
    return -1

def warn(n_iw_boxes, word_texts, font_style):
    n_iw_texts = len(word_texts)
    def print_warning(level):
        if level == 'TOUCH' or level[-7:] == 'SERIOUS':
            print(font_style, ':', level,  ' ', ''.join(word_texts),
                ' coming as ', n_iw_boxes, ' boxes (Expected ', n_iw_texts, ')')

    if n_iw_boxes > n_iw_texts:
        if n_iw_texts == 1:
            if n_iw_boxes == 2:
                if word_texts[0] not in '?!="॥':
                    if contains_vattu_haver(word_texts):
                        print_warning('VATTUERS')
                    else:
                        print_warning('SPLIT')
            else:
                print_warning('FRAGMENTS')    
        elif n_iw_boxes == n_iw_texts + 1:
            if word_texts[-1] != 'ః':
                if contains_vattu_haver(word_texts):
                    print_warning('VATTUERS SERIOUS')
                else:
                    print_warning('SPLIT SERIOUS')
        else:
            print_warning('FRAGMENTS SERIOUS')
    elif n_iw_boxes < n_iw_texts:
        if n_iw_texts == 2:
            print_warning('TOUCH')
        else:
            print_warning('TOUCH SERIOUS')