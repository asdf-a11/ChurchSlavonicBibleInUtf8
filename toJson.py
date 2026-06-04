import os
import json
import re
import unicodedata

book_order = {
    # --- OLD TESTAMENT ---
    "Кни́га_пе́рваѧ_мѡѷсе́ова_бытїѐ.txt": 1,
    "Кни́га_втора́ѧ_мѡѷсе́ова_и҆схо́дъ.txt": 2,
    "Кни́га_тре́тїѧ_мѡѷсе́ова_леѵі́тъ.txt": 3,
    "Кни́га_четве́ртаѧ_мѡѷсе́ова_чи́сла.txt": 4,
    "Кни́га_пѧ́таѧ_мѡѷсе́ова_второзако́нїе.txt": 5,
    "Кни́га_і҆исꙋ́са_наѵи́на.txt": 6,
    "Кни́га_сꙋді́й_і҆и҃левыхъ.txt": 7,
    "Кни́га_рꙋ́ѳь.txt": 8,
    "Кни́га_пе́рваѧ_ца́рствъ.txt": 9,
    "Кни́га_втора́ѧ_ца́рствъ.txt": 10,
    "Кни́га_тре́тїѧ_ца́рствъ.txt": 11,
    "Кни́га_четве́ртаѧ_ца́рствъ.txt": 12,
    "Кни́га_пе́рваѧ_паралїпоме́нѡнъ.txt": 13,
    "Кни́га_втора́ѧ_паралїпоме́нѡнъ.txt": 14,
    "Кни́га_пе́рваѧ_є҆́здры.txt": 15,
    "Кни́га_неемі́и.txt": 16,
    "Кни́га_втора́ѧ_є҆́здры.txt": 17,
    "Кни́га_тѡві́та.txt": 18,
    "Кни́га_і҆ꙋді́ѳъ.txt": 19,
    "Кни́га_є҆сѳи́рь.txt": 20,
    "Кни́га_і҆́ѡва.txt": 21,
    "Ѱалти́рь.txt": 22,
    "Кни́га_при́тчей_соломѡ́нихъ.txt": 23,
    "Кни́га_є҆кклесїа́ста_си́рѣчь_проповѣ́дника.txt": 24,
    "Кни́га_пѣ́снь_пѣ́сней_царѧ̀_соломѡ́на.txt": 25,
    "Кни́га_премⷣрости_соломѡ́ни.txt": 26,
    "Кни́га_премⷣрости_і҆исꙋ́са_сы́на_сїра́хова.txt": 27,
    "Кни́га_прⷪ҇ро́ка_и҆са́їи.txt": 28,
    "Кни́га_прⷪ҇ро́ка_і҆еремі́и.txt": 29,
    "Кни́га_пла́чь_і҆еремі́евъ.txt": 30,
    "Кни́га_посла́нїе_і҆еремі́ино.txt": 31,
    "Кни́га_прⷪ҇ро́ка_варꙋ́ха.txt": 32,
    "Кни́га_прⷪ҇ро́ка_і҆езекі́илѧ.txt": 33,
    "Кни́га_прⷪ҇ро́ка_данїи́ла.txt": 34,
    "Кни́га_прⷪ҇ро́ка_ѡ҆сі́и.txt": 35,
    "Кни́га_прⷪ҇ро́ка_і҆ѡи́лѧ.txt": 36,#Кни́га_прⷪ҇ро́ка_і҆ѡі́лѧ.txt
    "Кни́га_прⷪ҇ро́ка_а҆мѡ́са.txt": 37,
    "Кни́га_прⷪ҇ро́ка_а҆вді́а.txt": 38,
    "Кни́га_прⷪ҇ро́ка_і҆ѡ́ны.txt": 39,
    "Кни́га_прⷪ҇ро́ка_мїхе́а.txt": 40,
    "Кни́га_прⷪ҇ро́ка_наꙋ́ма.txt": 41,
    "Кни́га_прⷪ҇ро́ка_а҆ввакꙋ́ма.txt": 42,
    "Кни́га_прⷪ҇ро́ка_софо́нїи.txt": 43,
    "Кни́га_прⷪ҇ро́ка_а҆гге́а.txt": 44,
    "Кни́га_прⷪ҇ро́ка_заха́рїи.txt": 45,
    "Кни́га_прⷪ҇ро́ка_малахі́и.txt": 46,
    "Кни́га_пе́рваѧ_маккаве́йскаѧ.txt": 47,
    "Кни́га_втора́ѧ_маккаве́йскаѧ.txt": 48,
    "Кни́га_тре́тїѧ_маккаве́йскаѧ.txt": 49,
    "Кни́га_тре́тїѧ_є҆́здры.txt": 50,

    # --- NEW TESTAMENT ---
    "Ѿ_матѳе́а_ст҃о́е_бл҃говѣствова́нїе.txt": 51,
    "Ѿ_ма́рка_ст҃о́е_бл҃говѣствова́нїе.txt": 52,
    "Ѿ_лꙋкѝ_ст҃о́е_бл҃говѣствова́нїе.txt": 53,
    "Ѿ_і҆ѡа́нна_ст҃о́е_бл҃говѣствова́нїе.txt": 54,
    "Дѣѧ̑нїѧ_ст҃ы́хъ_а҆пⷭ҇лъ.txt": 55,
    "Собо́рное_посла́нїе_і҆а́кѡвле.txt": 56,
    "Собо́рное_посла́нїе_пе́рвое_ст҃а́гѡ_а҆пⷭ҇ла_петра̀.txt": 57,
    "Собо́рное_посла́нїе_второ́е_ст҃а́гѡ_а҆пⷭ҇ла_петра̀.txt": 58,
    "Собо́рное_посла́нїе_пе́рвое_ст҃а́гѡ_а҆пⷭ҇ла_і҆ѡа́нна_бг҃осло́ва.txt": 59,
    "Собо́рное_посла́нїе_второ́е_ст҃а́гѡ_а҆пⷭ҇ла_і҆ѡа́нна_бг҃осло́ва.txt": 60,
    "Собо́рное_посла́нїе_тре́тїе_ст҃а́гѡ_а҆пⷭ҇ла_і҆ѡа́нна_бг҃осло́ва.txt": 61,
    "Собо́рное_посла́нїе_і҆ꙋ́дино.txt": 62,
    "Посла́нїе_къ_ри́млѧнѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 63,
    "Посла́нїе_пе́рвое_къ_корі́нѳѧнѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 64,
    "Посла́нїе_второ́е_къ_корі́нѳѧнѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 65,
    "Посла́нїе_къ_гала́тѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 66,
    "Посла́нїе_ко_є҆фесе́ємъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 67,
    "Посла́нїе_къ_фїлїпписі́ємъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 68,
    "Посла́нїе_къ_колосса́ємъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 69,
    "Посла́нїе_пе́рвое_къ_солꙋ́нѧнѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 70,
    "Посла́нїе_второ́е_къ_солꙋ́нѧнѡмъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 71,
    "Посла́нїе_пе́рвое_къ_тїмоѳе́ю_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 72,
    "Посла́нїе_второ́е_къ_тїмоѳе́ю_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 73,
    "Посла́нїе_къ_ті́тꙋ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 74,
    "Посла́нїе_къ_фїлимо́нꙋ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 75,
    "Посла́нїе_ко_є҆вре́ємъ_ст҃а́гѡ_а҆пⷭ҇ла_па́ѵла.txt": 76,
    "А҆пока́лѷѱїсъ_ст҃а́гѡ_і҆ѡа́нна_бг҃осло́ва.txt": 77
}

def generate_slavonic_numbers(max_val=176):
    ones = {1: 'а', 2: 'в', 3: 'г', 4: 'д', 5: 'є', 6: 'ѕ', 7: 'з', 8: 'и', 9: 'ѳ'}
    tens = {10: 'і', 20: 'к', 30: 'л', 40: 'м', 50: 'н', 60: 'ѯ', 70: 'о', 80: 'п', 90: 'ч'}
    hundreds = {100: 'р'}
    
    titlo = '\u0483'
    numeral_list = []
    
    for n in range(1, max_val + 1):
        h_val = (n // 100) * 100
        t_val = ((n % 100) // 10) * 10
        o_val = n % 10
        
        base_str = ""
        if h_val:
            base_str += hundreds[h_val]
            
        # 11-19 rule: ones digit comes before the tens digit (і)
        if t_val == 10 and o_val > 0:
            base_str += ones[o_val] + tens[10]
        else:
            if t_val:
                base_str += tens[t_val]
            if o_val:
                base_str += ones[o_val]
                
        # Insert titlo right after the first letter (matching 'л҃д')
        if base_str:
            slavonic_num = base_str[0] + titlo + base_str[1:]
            numeral_list.append(unicodedata.normalize('NFC', slavonic_num))
            
    return numeral_list

# Generate the list
slavonic_verses = generate_slavonic_numbers(176)



bookList = []

# Ensure the output directory exists or just read from 'Books'
fileNameList = []
if os.path.exists('Books'):
    for filename in os.listdir('Books'):
        if filename.endswith('.txt'):
            fileNameList.append(filename)
            with open(os.path.join('Books', filename), 'r', encoding='utf-8') as file:
                contents = file.read()
   
                
                # Split by Chapter marker
                chapters = contents.split("Глава̀")
                chapters[-1] = chapters[-1].split("This is a translation")[0] # Remove copywright stuff
                print(f"File Name: {filename} | Total Chapters: {len(chapters) - 1}")
                chapters = chapters[1:]  # Remove the introduction/preface split
                
                #([.,!?;:()«»])'

                chapterList = []
                
                for ch_idx, chapter in enumerate(chapters):
                    versesList = []
                    # Prepend the marker back if you want, or just parse the text
                    #chapter_text = chapter
                    startIndex = 0
                    while startIndex < len(chapter):                        
                        if chapter[startIndex] == ".":
                            startIndex += 1
                            break
                        startIndex += 1
                    chapter_text = chapter[startIndex:]
                    chapter_text = chapter_text.replace("\n", "")
                    chapter_text = unicodedata.normalize('NFC', chapter_text)
                    
  
                    #NUMERAL_RE = r'([авгдєѕзиѳіклмнѯопрстуфхѱѡ]+҃[авгдєѕзиѳіклмнѯопрстуфхѱѡ]*)'
                    #NUMERAL_RE = slavonic_verses
                    #verse_parts = []
                    #for i in slavonic_verses:
                    #    l = chapter_text.split(i)
                    #    b = l[0]
                    #    verse_parts.append(b)
                    #    if len(l) == 1:
                    #        break
                    #    chapter_text = "".join(l[1:])
                    #verse_parts = re.split(NUMERAL_RE, chapter_text)
                    #print([repr(x) for x in slavonic_verses])
                    #print([len(x) for x in slavonic_verses])
                    #pattern = "[" + re.escape("".join(slavonic_verses)) + "]"
                    #verse_parts = re.split(pattern, chapter_text)

                    verse_parts = []

                    for marker in slavonic_verses[1:]:
                        pos = chapter_text.find(marker)

                        if pos == -1:
                            continue

                        verse_parts.append(chapter_text[:pos])
                        chapter_text = chapter_text[pos + len(marker):]

                    verse_parts.append(chapter_text)

                    for idx,i in enumerate(verse_parts):
                        #if idx % 2 == 1:
                        #    continue # dont want verse deliminators in the text so jump over them
                        versesList.append({
                            "verse": (idx)+1,
                            "text": i
                        })
                    
                    chapterList.append({
                        "chapter": ch_idx+1,
                        "verses": versesList
                    })

                bookList.append({
                    "name": filename.replace(".txt","").replace("_"," "),
                    "chapters": chapterList
                })
    bookListWithOrder = [0] * len(bookList)
    for book in bookList:
        n = unicodedata.normalize('NFC', book["name"].replace(" ","_"))
        #try:
        o = book_order[unicodedata.normalize('NFC', n+".txt")]
        bookListWithOrder[o-1] = book
        #except Exception:
        #    print(n+".txt", "А҆пока́лѷѱїсъ_ст҃а́гѡ_і҆ѡа́нна_бг҃осло́ва.txt" == n+".txt")
                  
    jsonOut = {
        "translation": "CSlElizabeth-CS: 1757 Church Slavonic Elizabeth Bible (Original Script)",
        "books": bookListWithOrder
    }
    # Write out to the JSON file with utf-8 encoding to preserve Cyrillic text
    with open("CSlElizabeth-CS.json", "w", encoding='utf-8') as f:
        json.dump(jsonOut, f, ensure_ascii=False, indent=4)
    print(fileNameList)
else:
    raise Exception("Error")