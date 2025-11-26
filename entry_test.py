import graphics as gf
window_size = 800
win = gf.GraphWin('bar do patrick', window_size * 1.2, window_size)


def generate_team(order):
    input_label.setText(f'Digite o nome do time {order}')
    team_name = get_text_input()
    input_label.setText(f'Digite o número de jogadores do time {team_name}')
    n = int(get_text_input())
    players = []
    for i in range(n):
        input_label.setText(f'Digite o nome do jogador {i + 1}')
        players.append(get_text_input())
                
    return players


def get_text_input():
    while True:
        key = win.getKey()
        if key == 'Return' and nome_input.getText() != '':
            text = nome_input.getText()
            nome_input.setText('')
            break
    return text


input_label = gf.Text(gf.Point(450, 300), '')
input_label.draw(win)
nome_input = gf.Entry(gf.Point(450, 350), 10)
nome_input.setFill("white")
nome_input.setSize(25)
nome_input.draw(win)

players = generate_team(1)

input_label.setText(str(players))
nome_input.undraw()
win.getMouse()
