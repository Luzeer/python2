import random

def theme_choice():
    choice = input('Нужно выбрать тему.\nТема 1: "Еда в голодные будни" \nТема 2: "В мире животных" \nТема 3: "Сектор-приз: для самых умных"\nВведите номер: ')
    if choice == '1':
        file = '1.txt'
    elif choice == '2':
        file = '2.txt'
    else:
        file = '3.txt'
    return file

def open_file():
    file = theme_choice()
    with open (file, encoding = 'utf-8') as f:
        words = f.read().lower()
    words = words.split('\n')
    word = random.choice(words)
    return word


def work_new_word(word):
    new_word = []
    for i in range(len(word)):
        new_word.append('_')
    for i in range(len(new_word)):
        print(new_word[i], end=' ')
    print()
    return new_word


def guess_letter (new_word, word):
    life = len(word)
    while life >= 0 and ''.join(new_word) != word:
        letter = input('Предположите, какая тут буковка может быть: ').lower()
        if letter in word:
            for i in range(len(word)):
                if letter == word[i]:
                    new_word[i] = letter
            print('Получилось, играем дальше...',' '.join(new_word))
        else:
            print ('Упс, если бы тут был человечек, он стал бы на шаг ближе к смерти(((')
            life -= 1
            if life == 1:
                print('Осталось 1 попытка')
            elif life in [2, 3, 4]:
                print('Осталось ', life, ' попытки')
            else:
                print('Осталось ', life, ' попыток')
    if (''.join(new_word) == word):
        print('You Win!')
        return new_word
    print ('Увы!!! Человечек не спасен')
                                   
def main():
    print('Сыграем? Это "Виселица". Правила знакомы всем. Поехали!')
    word = open_file()
    print('Проверка', word) 
    new_word = work_new_word(word)
    new_word = guess_letter(new_word, word)

main()
