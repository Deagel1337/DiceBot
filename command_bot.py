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

    def add_commands(self):
        @self.command(name="roll",pass_context=True,aliases=["r"])
        # Example !roll 3w10 3 dices with 1 - 10 numbers
        async def roll(ctx,dice_roll):
            
                number_dices = dice_roll.split('w')
                sum = 0             
                    
                result_throws = []
            
                # Handle the extra numbers
                more_extra_numbers = number_dices[1].split("+")
                positive_numbers = []
                negative_numbers = []
                for x in range(0,len(more_extra_numbers)):
                    if "-" in more_extra_numbers[x]:
                        negative_numbers_collection = more_extra_numbers[x].split("-")                      
                        for i in range(1,len(negative_numbers_collection)):
                            negative_numbers.append(int(negative_numbers_collection[i]))
                            positive_numbers.append(int(negative_numbers_collection[i-1]))
                    else:                       
                        positive_numbers.append(int(more_extra_numbers[x])) if x != 0 else 0
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
                # Depends on the number of dices    
              
                name= "Your "+dice_roll+" throw" + " {0.author.name}".format(ctx.message)
                if len(result_throws) > 1:
                    if extra_number != 0:
                        value = result_string+" {0} = {1}".format(extra_number,sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        value = result_string+" = {0}".format(str(sum))
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                else:
                    if extra_number != 0:
                        value = result_string +" {0} = {1}".format(extra_number,sum)
                        embedVar.add_field(name=name,value=value,inline=False)
                        await ctx.send(embed=embedVar)
                    else:
                        embedVar.add_field(name=name,value=result_string,inline=False)
                        await ctx.send(embed=embedVar)
            

    def add_events(self):
        pass
                
            


