from discord.ext import commands
import discord
import random
import asyncio
import json

class CommandBot(commands.Bot):
    intents = discord.Intents.default()
    intents.members = True
    sum = 0
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=self.intents,*args,**kwargs)
        self.add_commands()
        self.add_events()

    def find_first_operand(self,number_string):
        for character in number_string:
            if not character.isnumeric():
                return character
    
    def sort_numbers(self,numbers_list,character,positive_numbers,negative_numbers):
        numbers_collection = numbers_list.split(character)
        if numbers_collection[0] != '':
            positive_numbers.append(int(numbers_collection[0])) if character == "-" else negative_numbers.append(int(numbers_collection[0]))
        for i in range(1,len(numbers_collection)):
            negative_numbers.append(int(numbers_collection[i])) if character == "-" else positive_numbers.append(int(numbers_collection[i]))

    
    def calculate_number(self,positive_numbers,negative_numbers):
        extra_number = ""
        for x in positive_numbers:
            extra_number += " + {0}".format(x)
            self.sum += x
        for x in negative_numbers:
            self.sum -= x
            extra_number += " - {0}".format(x)
        return extra_number
    
    def get_number_of_dices(self,number_dices):
        max_number = ""
        for x in range(0,len(number_dices[1])):
            if number_dices[1][x].isnumeric():
                max_number += number_dices[1][x]
            else:
                break
        return  int(max_number)
    
    def create_embed_response(self,embedVar,result_string,name,extra_number = ""):
        value = result_string+" {0} = {1}".format(extra_number,sum)
        embedVar.add_field(name=name,value=value,inline=False)
        
        
    def add_commands(self):
        @self.command(name="roll",pass_context=True,aliases=["r"])
        # Example !roll 3w10 3 dices with 1 - 10 numbers
        async def roll(ctx,dice_roll):
                if dice_roll[0].isnumeric() == False:
                    new_string = "1{0}".format(dice_roll)
                    dice_roll = new_string
                number_dices = dice_roll.split('w') if 'w' in dice_roll else dice_roll.split('d')

                result_throws = []
            
                # Handle the extra numbers
                is_negative = False
                if self.find_first_operand(number_dices[1]) == "+":
                    more_extra_numbers = number_dices[1].split("+")
                else:
                    more_extra_numbers = number_dices[1].split("-")
                    is_negative = True
            
                positive_numbers = []
                negative_numbers = []
                
                # Sorts extra numbers by positive and negatives
                for x in range(1,len(more_extra_numbers)):
                    if "-" in more_extra_numbers[x]:
                        self.sort_numbers(more_extra_numbers[x],"-",positive_numbers,negative_numbers)
                    elif "+" in more_extra_numbers[x]:
                        self.sort_numbers(more_extra_numbers[x],"+",positive_numbers,negative_numbers)               
                    else:
                        # Handles the first number correctly              
                        if is_negative == False:       
                            positive_numbers.append(int(more_extra_numbers[x])) if x!= 0 else 0
                        else:
                            negative_numbers.append(int(more_extra_numbers[x])) if x!= 0 else 0

                extra_number = self.calculate_number(positive_numbers,negative_numbers)               
        
                # Split the extra numbers away
                max_range_number = self.get_number_of_dices(number_dices)
                
                # Dices are thrown
                number_of_dices = int(number_dices[0])
                for x in range(0,number_of_dices):
                    throw = random.randint(1,max_range_number)
                    result_throws.append(throw)

                # Constructs string that will return to discord
                result_string = " "
                
                for x in range(0,len(result_throws)):
                    if len(result_throws) > 1:
                        result_string+=(str(result_throws[x])+" + " if x < len(result_throws)-1 else str(result_throws[x]))
                    else:
                        result_string+=str(result_throws[0])
                    self.sum  += int(result_throws[x])
                
                embedVar = discord.Embed(title="The die is cast!",description="Throw your dice!")
                # Output depening on the inputformat    
                name= "Your "+dice_roll+" throw" + " {0.author.name}".format(ctx.message)
                if len(result_throws) > 1:
                    # If output is !r 1w10+3+...
                    if len(extra_number) != 0:
                        value = result_string+" {0} = {1}".format(extra_number,self.sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        value = result_string+" = {0}".format(self.sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                else:
                    if len(extra_number) != 0:
                        value = result_string +" {0} = {1}".format(extra_number,self.sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar.add_field(name=name,value=result_string,inline=False)
                        await ctx.send(embed=embedVar)
                self.sum = 0;
            

    def add_events(self):
        pass
                