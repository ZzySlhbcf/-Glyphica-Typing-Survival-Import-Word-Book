import pandas as pd
import re
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
word_list = [[] for i in range(4, 11)]


def csv_writer():
    dictionary = {}
    for i in range(4, 11):
        dictionary[f"{i}-LETTER WORDS"] = word_list[i-4]
    df_write = pd.DataFrame.from_dict(dictionary, orient='index')
    df_write = df_write.T
    df_write.to_csv("schinese_wordlist.csv", encoding='utf-8', index=False)


def word_checker(word: str) -> bool:
    if len(word) > 10 or len(word) < 4:
        return False
    for letter in word:
        if letter not in letters:
            return False
    return True


def no_comma(chinese: str) -> list:
    translation_list = []
    chinese = chinese.replace(" ", "")
    chinese_translations = re.split(r'；|;', chinese)
    for translation in chinese_translations:
        translation_list.append(re.split(r'，|,', translation)[-1])
    translation_list.sort(key=lambda i: len(i), reverse=False)
    if len(translation_list) <= 3:
        return ["；".join(translation_list)]
    res = []
    while len(translation_list) > 3:
        print(translation_list)
        if len(translation_list) == 4:
            res.append("；".join(translation_list[0:2]))
            res.append("；".join(translation_list[2:]))
            break
        res.append("；".join(translation_list[0:3]))
        translation_list = translation_list[3:]
    return res


def revise_translation(translations: list) -> str:
    translation_list = []
    for translation in translations:
        pos_translation = translation.split(". ")
        if len(pos_translation) < 2:
            continue
        chinese_translation_list = no_comma(pos_translation[1])
        for chinese_translation in chinese_translation_list:
            translation_list.append(pos_translation[0]+"."+chinese_translation)
    return translation_list


if __name__ == "__main__":
    df_read = pd.read_csv("001.csv", encoding='utf-8')
    for i in range(len(df_read)):
        row = df_read.iloc[i]
        word = row[0].lower()
        if not word_checker(word):
            continue
        try:
            translations = row[1].split('\n')
        except:
            continue
        translation_list = revise_translation(translations)
        if translation_list == []:
            continue
        for translation in translation_list:
            word_translation = word+" "+translation
            word_list[len(word)-4].append(word_translation)
    csv_writer()
