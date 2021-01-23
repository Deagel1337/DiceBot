from discord.ext import commands
import discord
import random
import asyncio
import json

class CommandBot(commands.Bot):
    intents = discord.Intents.default()
    intents.members = True
    def __init__(self,*args,**kwargs):
        super().__init__(command_prefix="!",intents=self.intents,*args,**kwargs)
        self.add_commands()
        self.add_events()

    def find_first_operand(self,number_string):
        for character in number_string:
            if not character.isnumeric():
                return character
    

    

    def add_commands(self):
        @self.command(name="roll",pass_context=True,aliases=["r"])
        # Example !roll 3w10 3 dices with 1 - 10 numbers
        async def roll(ctx,dice_roll):
                if dice_roll[0].isnumeric() == False:
                    new_string = "1{0}".format(dice_roll)
                    dice_roll = new_string
                number_dices = dice_roll.split('w') if 'w' in dice_roll else dice_roll.split('d')

                sum = 0             
                    
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
                        negative_numbers_collection = more_extra_numbers[x].split("-")
                        if negative_numbers_collection[0] != '':
                            positive_numbers.append(int(negative_numbers_collection[0]))
                        for i in range(1,len(negative_numbers_collection)):
                            negative_numbers.append(int(negative_numbers_collection[i])) 
                    elif "+" in more_extra_numbers[x]:
                        positive_numbers_collection = more_extra_numbers[x].split("+")
       
                        negative_numbers.append(int(positive_numbers_collection[0]))
                        for i in range(1,len(positive_numbers_collection)):
                            positive_numbers.append(int(positive_numbers_collection[i]))                
                    else:              
                        if is_negative == False:       
                            positive_numbers.append(int(more_extra_numbers[x])) if x!= 0 else 0
                        else:
                            negative_numbers.append(int(more_extra_numbers[x])) if x!= 0 else 0
                extra_number = ""               
               
                for x in positive_numbers:
                    extra_number += " + {0}".format(x)
                    sum += x
                for x in negative_numbers:
                    sum -= x
                    extra_number += " - {0}".format(x)

                # Split the extra numbers away
                number_of_dices = int(number_dices[0])
                max_number = ""
                for x in range(0,len(number_dices[1])):
                    if number_dices[1][x].isnumeric():
                        max_number += number_dices[1][x]
                    else:
                        break
                max_range_number =  int(max_number)
                
                # Dices are thrown
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
                    sum  += int(result_throws[x])
                
                embedVar = discord.Embed(title="The die is cast!",description="Throw your dice!")
                # Output depening on the inputformat    
                name= "Your "+dice_roll+" throw" + " {0.author.name}".format(ctx.message)
                if len(result_throws) > 1:
                    # If output is !r 1w10+3+...
                    if len(extra_number) != 0:
                        value = result_string+" {0} = {1}".format(extra_number,sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        value = result_string+" = {0}".format(str(sum))
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                else:
                    if len(extra_number) != 0:
                        value = result_string +" {0} = {1}".format(extra_number,sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar.add_field(name=name,value=result_string,inline=False)
                        await ctx.send(embed=embedVar)
            

    def add_events(self):
        pass
                
            


