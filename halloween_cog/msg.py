candy_emoji = "🍬"

class error():
    no_candy = "**❤️ {}, you don't have enough 🍬candy.**"

class embed():
    prize_context = """
    **__🎉{}__**

    **Candy Won: {}**``{}``
    """

    footer_1 = "💛Goldy Bot - 🎃Halloween Extenstion (2021)"

class boo():
    class error():
        cooldown = "**❤️ Don't scare yourself too much kid. Try again in __{}__**"
        
    class embed():
        gif_url = "https://design4users.com/wp-content/uploads/2016/10/halloween_animation_bat.gif"

class treat():
    class error():
        cooldown = "**❤️ Too much candy is bad for you kid. Try again in __{}__**"

    class embed():
        candy_kid_gif = "https://media.giphy.com/media/3otPoI5hCxUVX63Vcc/giphy.gif"
        steal_gif = "https://media.giphy.com/media/fkZD8aqDpkSjqF8X4p/giphy.gif"

        steal_context = '''
        **{}, That neighbour stole your candy!**

        **Candy Stolen: {}**``{}``
        '''

        won_context = '''
        **{}, They offered you some candy.**
        
        **Candy Given: {}**``{}``
        '''

class scary():
    you_sure = "**{}, are you sure? There's some real creepy stuff here.**"

class battable():
    their_not_battable = "**💛 {}, their not 🦇battable!**"
    toggle_on = "**💚 {}, member's are now able to sent you 🦇bats.**"
    toggle_off = "**💛 {}, no one can send you 🦇bats now. Good choice, this is the safer option.**"

    your_not_battable = "**💙 {}, don't worry you aren't 🦇battable. *If for some reason you want to allow members to send you 🦇bats, try this command --> ``!battable on``.***"
    your_battable = "**💛 {}, yes you are in deed 🦇battable. *To stop members from sending you 🦇bats, try this command --> ``!battable off``.***"

class bat():
    class failed():
        not_battable = battable.their_not_battable

    sent = "**💚 {}, 🦇bat has been dispatched and will be arriving soon.**"

class bal():
    class embed():
        main_context = """
        **__{}__ **
        
        **Candy: {}**``{}``
        """

        footer_context = "🍬To gain candy try commands like '!boo', '!treat' and '!cram'."