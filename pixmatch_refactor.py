import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Configura la página de Streamlit con un título, ícono y layout específico.
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# Define variables para el manejo de directorios y archivos.
vDrive = os.path.splitdrive(os.getcwd())[0]
vpth = "./"


# Cadenas HTML que se utilizarán para mostrar emojis y barras horizontales en la UI.
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"    # thin divider line

# Estilos CSS para personalizar los botones en Streamlit.
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Inicializa variables de estado de sesión para manejar el estado a lo largo del juego.
mystate = st.session_state
if "expired_cells" not in mystate: mystate.expired_cells = []
if "myscore" not in mystate: mystate.myscore = 0
if "plyrbtns" not in mystate: mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate: mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate: mystate.emoji_bank = []
if "GameDetails" not in mystate: mystate.GameDetails = ['Medium', 6, 7, '']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name

#se agregan dos estados nuevos al juego: el estado de intentos incorrectos y de finalización en caso de perder, estas variables estarán presentes en la función NewGame y pressedCheck
if "wrong_attempts" not in mystate: mystate.wrong_attempts = 0
if "game_over" not in mystate: mystate.game_over = False


def ReduceGapFromPageTop(wch_section = 'main page'):  # Ajusta el espacio superior de la página principal o la barra lateral para mejorar la estética.

    if wch_section == 'main page': st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True) # main area
    elif wch_section == 'sidebar': st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True) # sidebar
    
    elif wch_section == 'all': 
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True) # main area
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True) # sidebar


    
def Leaderboard(what_to_do): #Gestiona un leaderboard leyendo y escribiendo en un archivo JSON. Actualiza, crea y muestra el leaderboard basado en los nombres de los jugadores y sus puntuaciones.
    # Se verifica si el archivo 'leaderboard.json' no existe en el directorio especificado.
    # Si no existe y el jugador ha proporcionado su nombre (GameDetails[3] no está vacío),
    # se crea un archivo JSON vacío para almacenar los datos del tablero de líderes.
    if what_to_do == 'create':
        if mystate.GameDetails[3] != '': 
            if os.path.isfile(vpth + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))     # write file

    elif what_to_do == 'write': #Esta opción se utiliza para actualizar el tablero de líderes con los nuevos puntajes.
        if mystate.GameDetails[3] != '':       # solo se escribe si se ha proporcionado un nombre
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))    # Carga los datos existentes del tablero de líderes.
                leaderboard_dict_lngth = len(leaderboard)
                    
                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3], 'HighestScore': mystate.myscore} 
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # # Ordena el diccionario de líderes por puntaje más alto de forma descendente

                # Si hay más de 3 registros en el tablero, elimina los últimos. (corregido para los últimos 4 jugadores)
                if len(leaderboard) > 4:
                    for i in range(len(leaderboard)-4 ): leaderboard.popitem()    

                # Guarda el diccionario actualizado de nuevo en el archivo JSON.
                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))     # write file

    elif what_to_do == 'read': #Esta opción se utiliza para leer y mostrar los datos del tablero de líderes.
        if mystate.GameDetails[3] != '':       # record in leaderboard only if player name is provided
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))    # read file
                    
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                sc0, sc1, sc2, sc3, sc4 = st.columns((2,3,3,3,3))
                rknt = 0

                ## Configura la presentación visual de los mejores puntajes en columnas.
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            sc1.write(f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2: sc2.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3: sc3.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 4: sc4.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]") #añadí esto para mostrar al cuarto jugador


def InitialPage():

    # Configura y muestra elementos en la barra lateral.
    with st.sidebar:
        st.subheader("🖼️ Pix Match:") 
        st.markdown(horizontal_bar, True) # Utiliza HTML para mostrar una barra horizontal como divisor.

         # Carga y muestra una imagen en la barra lateral, ajustando su tamaño
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')

    # # Configura y muestra las reglas del juego y las instrucciones de juego en la página principal.
    hlp_dtl = f"""<span style="font-size: 26px;">
    <ol>
    <li style="font-size:15px";>Game play opens with (a) a sidebar picture and (b) a N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
    <li style="font-size:15px";>You need to match the sidebar picture with a grid picture button, by pressing the (matching) button (as quickly as possible).</li>
    <li style="font-size:15px";>Each correct picture match will earn you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match will earn you <strong>-1</strong> point.</li>
    <li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed seconds interval (Easy=8, Medium=6, Hard=5). Each regeneration will have a penalty of <strong>-1</strong> point</li>
    <li style="font-size:15px";>Each of the grid buttons can only be pressed once during the entire game.</li>
    <li style="font-size:15px";>The game completes when all the grid buttons are pressed.</li>
    <li style="font-size:15px";>At the end of the game, if you have a positive score, you will have <strong>won</strong>; otherwise, you will have <strong>lost</strong>.</li>
    </ol></span>""" 

    # Configura dos columnas para mostrar visualmente las reglas y una imagen de ayuda.
    sc1, sc2 = st.columns(2)
    random.seed()
    GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
    GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
    sc2.image(GameHelpImg, use_column_width='auto')

    sc1.subheader('Rules | Playing Instructions:')
    sc1.markdown(horizontal_bar, True)  # Muestra un divisor horizontal para organizar visualmente el contenido.
    sc1.markdown(hlp_dtl, unsafe_allow_html=True) # Muestra las reglas del juego en formato HTML.
    st.markdown(horizontal_bar, True) # Muestra otro divisor horizontal para organizar visualmente el contenido.

    author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>" #auto propaganda
    st.markdown(author_dtl, unsafe_allow_html=True)

def ReadPictureFile(wch_fl):
    try:
        pxfl = f"{vpth}{wch_fl}" # Construye la ruta completa al archivo de imagen.
        return base64.b64encode(open(pxfl, 'rb').read()).decode() 

    except: return "" # Si ocurre un error (archivo no encontrado, error de permisos, etc.), devuelve una cadena vacía.

def PressedCheck(vcell):  # Comprueba si el botón especificado por 'vcell' no ha sido presionado anteriormente.
    if mystate.plyrbtns[vcell]['isPressed'] == False: # Marca el botón como presionado. 
        mystate.plyrbtns[vcell]['isPressed'] = True 
        mystate.expired_cells.append(vcell)  # Agrega la celda al listado de celdas expiradas (ya utilizadas).
 
         # Comprueba si el emoji en el botón coincide con el emoji en la barra lateral.

        if mystate.plyrbtns[vcell]['eMoji'] == mystate.sidebar_emoji:
            mystate.plyrbtns[vcell]['isTrueFalse'] = True
            mystate.myscore += 5
            
            #aumenta la puntuación dependiendo del nivel de dificultad
            if mystate.GameDetails[0] == 'Easy': mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium': mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard': mystate.myscore += 1
        #en caso de ser falso, resta un punto
        else:
            mystate.plyrbtns[vcell]['isTrueFalse'] = False
            mystate.myscore -= 1
            mystate.wrong_attempts += 1  # Increment the wrong attempts


            #se configuran la cantidad de turnos antes de perder el juego
            total_attempts_allowed = mystate.GameDetails[2]**2 // 2 + 1
            #cuando se superen estos turnos, el estado de juego cambia para así proceder a dar el mensaje de game over al usuario desde la función NewGame
            if mystate.wrong_attempts >= total_attempts_allowed:
                mystate.game_over = True
                st.experimental_rerun()



def ResetBoard():
     # Obtiene el número total de celdas por fila o columna desde el estado del juego.
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Selecciona un emoji aleatorio de la 'emoji_bank' para la barra lateral.
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank))-1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]
 
    sidebar_emoji_in_list = False # Flag para verificar si el emoji de la barra lateral está presente en algún botón.

    for vcell in range(1, ((total_cells_per_row_or_col ** 2)+1)): # Asigna un emoji aleatorio a cada celda que aún no ha sido presionada.
        rndm_no = random.randint(1, len(mystate.emoji_bank))-1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji: sidebar_emoji_in_list = True

    if sidebar_emoji_in_list == False:  # # Si el emoji de la barra lateral no está en ninguno de los botones activos, añádelo al azar
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2)+1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst)-1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji

def PreNewGame():
    # Establece el número total de celdas por fila o columna desde el estado del juego.
    total_cells_per_row_or_col = mystate.GameDetails[2]

    # Reinicia las listas de celdas expiradas y la puntuación del jugador.
    mystate.expired_cells = []
    mystate.myscore = 0

    #lista de emojis
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓', '👴', '👲', '👳'] 
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗', '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻', '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽', '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽', '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍', '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬', '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍', '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️', '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘', '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️', '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛', '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    #selecciona los emojis dependiendo de la dificultad de la partida
    random.seed()
    if mystate.GameDetails[0] == 'Easy':
        wch_bank = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Medium':
        wch_bank = random.choice(['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[wch_bank]

    elif mystate.GameDetails[0] == 'Hard':
        wch_bank = random.choice(['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs', 'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[wch_bank]


    # Reinicia el estado de los botones en el tablero.
    mystate.plyrbtns = {}
    for vcell in range(1, ((total_cells_per_row_or_col ** 2)+1)): mystate.plyrbtns[vcell] = {'isPressed': False, 'isTrueFalse': False, 'eMoji': ''}

def ScoreEmoji(): # Evalúa el puntaje actual almacenado en el estado del juego y retorna un emoji correspondiente.
    if mystate.myscore == 0: return '😐' #puntaje regular ... 
    elif -5 <= mystate.myscore <= -1: return '😏'
    elif -10 <= mystate.myscore <= -6: return '☹️'
    elif mystate.myscore <= -11: return '😖'
    elif 1 <= mystate.myscore <= 5: return '🙂'
    elif 6 <= mystate.myscore <= 10: return '😊'
    elif mystate.myscore > 10: return '😁' #puntaje muy bueno

def NewGame():

    #verificar inicialmnete si el juego está perdido 
    if mystate.game_over:
        st.error("Game Over! You have made too many incorrect attempts.") #imprimir mensaje al usuario de que perdió el juego
        if st.button("Return to Main Page"): 
            #reiniciar las variables de estado en caso de que el usuario vuelva a la página principal para que pueda volver a jugar. 
            mystate.runpage = Main
            mystate.wrong_attempts = 0  
            mystate.game_over = False  
            mystate.expired_cells = []  
            st.experimental_rerun()
        return
    
    else:
        ResetBoard() # Reinicia y configura el tablero para una nueva partida. 
        total_cells_per_row_or_col = mystate.GameDetails[2] # Obtiene el número total de celdas por fila o columna del estado del juego.

        ReduceGapFromPageTop('sidebar') # Ajusta el espacio en la parte superior de la barra lateral.
        with st.sidebar: # Muestra detalles del nivel de dificultad y un emoji representativo en la barra lateral.
            st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")
            st.markdown(horizontal_bar, True)

            st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True) 

            aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr") # Establece y maneja un auto-refresco basado en el intervalo de tiempo definido en la dificultad.
            if aftimer > 0: mystate.myscore -= 1 # Penaliza el puntaje cada vez que se refresca la página automáticamente.
    
            # Muestra el puntaje actual y la cantidad de celdas pendientes por presionar.
            st.info(f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2)-len(mystate.expired_cells)}") 

            st.markdown(horizontal_bar, True)
            if st.button(f"🔙 Return to Main Page", use_container_width=True): # Si se presiona el botón, se regresa a la página principal y se reinicia el juego.
                mystate.runpage = Main
                st.rerun()
    

    # Maneja la lectura del tablero de líderes.
    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Dafaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ", unsafe_allow_html=True)  # make button face big


    # Prepara y muestra el tablero de juego.
    for i in range(1, (total_cells_per_row_or_col+1)): # Itera sobre cada fila del tablero para configurar las columnas
        # Define la configuración de las columnas para cada fila, añadiendo padding derecho para separación visual
        tlst = ([1] * total_cells_per_row_or_col) + [2] # 2 = # [2] es para el padding derecho.
        # Almacena la configuración de las columnas en una variable global por fila
        globals()['cols' + str(i)] = st.columns(tlst)
    
    # Itera sobre cada celda del tablero para asignar botones y manejar eventos
    for vcell in range(1, (total_cells_per_row_or_col ** 2)+1): # Determina la fila a la que pertenece la celda actual basándose en su índice
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0
        # Repite las condiciones para asignar correctamente las celdas a las filas
        # Continúa para todas las filas necesarias hasta cubrir el tablero completo

        elif ((total_cells_per_row_or_col * 1)+1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2)+1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3)+1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4)+1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5)+1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6)+1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7)+1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8)+1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9)+1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)
            

        # Limpia el contenido previo antes de asignar un nuevo botón o emoji
        globals()['cols' + arr_ref][vcell-mval] = globals()['cols' + arr_ref][vcell-mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:  # Si la celda ha sido presionada, muestra el resultado de esa acción
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True: # Muestra un emoji de verificación si la selección fue correcta
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)
            
            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False: # Muestra un emoji de error si la selección fue incorrecta
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)

        else: # Asigna el emoji correspondiente al botón si aún no ha sido presionado
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell-mval].button(vemoji, on_click=PressedCheck, args=(vcell, ), key=f"B{vcell}")


    # Espacio adicional para mejorar la disposición visual en la interfaz
    st.caption('') # vertical filler
    st.markdown(horizontal_bar, True)

    # Finaliza el juego si todas las celdas han sido presionadas y procede con la lógica de conclusión
    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2):
        Leaderboard('write') # Registra los resultados en el tablero de líderes
        # Muestra animaciones según el resultado final del puntaje
        if mystate.myscore > 0: st.balloons()
        elif mystate.myscore <= 0: st.snow()
        # Pausa antes de reiniciar la página principal
        tm.sleep(5)
        mystate.runpage = Main
        st.rerun()

def Main():
    # Aplica CSS personalizado para reducir el ancho de la barra lateral, mejora la presentación visual.
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True)

    # Aplica colores personalizados a los botones definidos en el estilo global `purple_btn_colour`.
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    # Llama a la función `InitialPage()` que configura la página inicial del juego con instrucciones y opciones.
    InitialPage()

    # Bloque para configurar elementos interactivos en la barra lateral.
    with st.sidebar:
        # Opción para seleccionar el nivel de dificultad del juego, con 'Medium' como opción predeterminada.
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1, horizontal=True)

        # Campo para que el jugador ingrese su nombre y país, usado en el tablero de líderes.
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India', help='Optional input only for Leaderboard')

        # Botón para iniciar un nuevo juego. Al hacer clic, se configuran detalles específicos del juego basados en la dificultad.
        if st.button(f"🕹️ New Game", use_container_width=True):
            # Configuración del intervalo de tiempo y la cantidad de celdas según la dificultad elegida.
            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # Intervalo en segundos para la dificultad Fácil.
                mystate.GameDetails[2] = 6  # Total de celdas por fila/columna para Fácil.
            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # Intervalo para Media.
                mystate.GameDetails[2] = 7  # Celdas para Media.
            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # Intervalo para Difícil.
                mystate.GameDetails[2] = 8  # Celdas para Difícil.

            # Crea un nuevo tablero de líderes para la sesión actual si es necesario.
            Leaderboard('create')

            # Prepara el juego para una nueva partida, configurando el tablero y los estados necesarios.
            PreNewGame()

            # Establece `NewGame` como la próxima página a ejecutar y refresca la página para iniciar el juego.
            mystate.runpage = NewGame
            st.rerun()

        # Añade una barra horizontal para separar visualmente las secciones de la barra lateral.
        st.markdown(horizontal_bar, True)

# Verifica si `runpage` está definido en el estado del juego, si no, lo establece a `Main`.
if 'runpage' not in mystate:
    mystate.runpage = Main

# Ejecuta la función asignada a `runpage`, que inicialmente es `Main`, para cargar la página principal.
mystate.runpage()
