class HelpOperators:
    @staticmethod
    def find_first_operand(number_string):
        for character in number_string:
            if not character.isnumeric():
                return character
    
    @staticmethod
    def sort_numbers(numbers_list,character,positive_numbers,negative_numbers):
        numbers_collection = numbers_list.split(character)
        if numbers_collection[0] != '':
            positive_numbers.append(int(numbers_collection[0])) if character == "-" else negative_numbers.append(int(numbers_collection[0]))
        for i in range(1,len(numbers_collection)):
            negative_numbers.append(int(numbers_collection[i])) if character == "-" else positive_numbers.append(int(numbers_collection[i]))

    @staticmethod
    def get_number_of_dices(number_dices):
        max_number = ""
        for x in range(0,len(number_dices[1])):
            if number_dices[1][x].isnumeric():
                max_number += number_dices[1][x]
            else:
                break
        return  int(max_number)