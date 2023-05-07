from models import Word, Other_words

def dict_filling(dictionary1, dictionary2):
    
    ru_en_dict = [{'Птица': 'Bird'}, {'Медведь':'Bear'}, {'Школа':'School'},
                  {'Дерево':'Tree'}, {'Мяч':'Ball'}, {'Часы':'Clock'},
                  {'Здание':'Building'}, {'Мышь':'Mouse'}, {'Насекомое':'Insect'}, 
                  {'Любовь':'Love'}, {'Море':'Sea'}, {'Солнце':'Sun'}, 
                  {'Мир':'Peace'}, {'Дружба':'Friendship'}, {'Ветер':'Wind'},
                  {'Корабль':'Ship'}, {'Небо':'Sky'}, {'Облако':'Cloud'},
                  {'Счастье':'Happiness'},{'Кот':'Cat'}]

    other_words_list = ['Glory','Song','Variant','Power','Rain','Dog','Join','Sleep','Language','Ring',
                        'King','List','Paper','Pensil','Socks','Stone','Angel','Morning','Beaver','Son','Call',
                        'Result','Sister','Pipe','Green','Milk','Pink','Quake','Time','Flash','Close','Cute',
                        'Water','River','Lake','Fish','Trip','Beer','Item','Value','Question','Blue']
    
    for word_pair in ru_en_dict:
        word = Word(russian_word = list(word_pair.keys())[0], target_word = list(word_pair.values())[0])
        dictionary1.append(word)
    
    for othr_wrd in other_words_list:
        othr_word = Other_words(other_word = othr_wrd)
        dictionary2.append(othr_word)



