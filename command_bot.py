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
            number_dices = dice_roll.split('w',1)
            extra_number = 0
            sum = 0             
                
            result_throws = []
        
            # Handle the extra numbers
            
            if "+" in number_dices[1] :
                temp_num = number_dices[1].split("+",1)
                extra_number = int(temp_num[1])
                number_dices[1] = str(number_dices[1][0:number_dices[1].index('+')])
                sum += extra_number
            elif "-" in number_dices[1]:
                temp_num = number_dices[1].split("-",1)
                extra_number = int(temp_num[1])
                number_dices[1] = str(number_dices[1][0:number_dices[1].index('-')])
                sum -= extra_number
                extra_number*=-1
            
            # Dices are thrown
            for x in range(0,int(number_dices[0])):
                throw = random.randint(1,int(number_dices[1]))
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
            sign = " +" if extra_number > 0 else ""
            if len(result_throws) > 1:
                if extra_number != 0:
                    value = result_string+sign+" {0} = {1}".format(extra_number,sum)
                    embedVar.add_field(name="Your "+dice_roll+" throw",value=value,inline=False)
                    await ctx.send(embed=embedVar)
                else:
                    value = result_string+" = {0}".format(str(sum))
                    embedVar.add_field(name="Your "+dice_roll+" throw",value=value,inline=False)
                    await ctx.send(embed=embedVar)
            else:
                if extra_number != 0:
                    value = result_string +sign+" {0} = {1}".format(extra_number,sum)
                    embedVar.add_field(name="Your "+dice_roll+" throw",value=value,inline=False)
                    await ctx.send(embed=embedVar)
                else:
                    embedVar.add_field(name="Your "+dice_roll+" throw",value=result_string,inline=False)
                    await ctx.send(embed=embedVar)

    def add_events(self):
        pass
                
            


