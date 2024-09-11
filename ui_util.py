# UI dealie for the game

import streamlit

def qwerty_buttons(already_used:set, callback=None):
    result = None
    for row in "QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM.":
        columns = streamlit.columns(10)
        letter_index = 0
        for letter in row:
            column = columns[letter_index]
            if letter in already_used:
                column.button(letter, key=f"letter {letter}", disabled=True)
            else:
                b = column.button(letter, key=f"letter {letter}", on_click=callback)
                if b:
                    result = letter
            letter_index += 1
    # Show the space bar
    if " " in already_used:
        streamlit.button("<SPACE>", key="letter space", disabled=True)
    else:
        b = streamlit.button("<SPACE>", key="letter space", on_click=callback)
        if b:
            result = " "
    # Show the Hint button
    hint = streamlit.button("Hint", key="hint", on_click=callback)
    if hint:
        result = "hint"
    return result