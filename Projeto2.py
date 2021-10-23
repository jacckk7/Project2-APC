#####################################################################################################
###################################### Projeto 2 de APC #############################################
################################## Breno Costa Avelino Lima #########################################
#####################################################################################################

#####################################################################################################
#################################### functions definition ###########################################
#####################################################################################################

def atualiza_mesas(mesas_area, mesas_status, areas):
    arquivo = input()
    with open('Mesas/' + arquivo, 'r') as arq:
        for registro in arq:
            nome_mesa, area_mesa, status = registro.split(', ')
            nome_mesa = int(nome_mesa)
            status = status.strip('\n')
            mesas_area[nome_mesa] = area_mesa
            mesas_status[nome_mesa] = status
            if area_mesa not in areas:
                areas.append(area_mesa)
    
def atualiza_cardapio(cardapio):
    arquivo = input()
    with open('Cardapios/' + arquivo, 'r') as arq:
        for registro in arq:
            prato_ingredientes = registro.split(', ')
            prato_ingredientes[-1] = prato_ingredientes[-1].strip('\n')
            prato = prato_ingredientes[0]
            prato_ingredientes = prato_ingredientes[1:]
            cardapio[prato] = {}
            for item in prato_ingredientes:
                if item in cardapio[prato]:
                    cardapio[prato][item] += 1
                else:
                    cardapio[prato][item] = 1
    
def atualiza_estoque(estoque):
    arquivo = input()
    with open('Estoques/' + arquivo, 'r') as arq:
        for registro in arq:
            ingrediente, qnt = registro.split(', ')
            qnt = int(qnt.strip('\n'))
            if ingrediente in estoque:
                estoque[ingrediente] += qnt
            else:
                estoque[ingrediente] = qnt
    
def relatorio_mesas(mesas_area, mesas_status, areas):
    areas_order = sorted(areas)
    mesas_order = sorted(mesas_status)
    if len(mesas_area) != 0:
        for elemento in areas_order:
            print(f'area: {elemento}')
            count = 0
            for item in mesas_order:
                if mesas_area[item] == elemento:
                    print(f'- mesa: {item}, status: {mesas_status[item]}')
                    count = 1
            if count == 0:
                print('- area sem mesas')
    else:
        print('- restaurante sem mesas')
        
def relatorio_cardapio(cardapio):
    cardapio_order = sorted(cardapio)
    if len(cardapio) != 0:
        for elemento in cardapio_order:
            ingredientes_order = sorted(cardapio[elemento])
            print(f'item: {elemento}')
            for i in range(len(ingredientes_order)):
                print(f'- {ingredientes_order[i]}: {cardapio[elemento][ingredientes_order[i]]}')
    else:
        print('- cardapio vazio')
        
def relatorio_estoque(estoque):
    estoque_order = sorted(estoque)
    if len(estoque) != 0:
        for elemento in estoque_order:
            print(f'{elemento}: {estoque[elemento]}')
    else:
        print('- estoque vazio')
        
def tem_suf(i, cardapio, estoque):
    for elemento in cardapio[i]:
        if elemento not in estoque or estoque[elemento] < cardapio[i][elemento]:
            return True
        
    return False

def fazer_pedido(mesas_status, cardapio, estoque, pedidos, pedidos_tempo):
    n, i = input().split(', ')
    n = int(n)
    if n not in mesas_status:
        print(f'erro >> mesa {n} inexistente')
    elif mesas_status[n] == 'livre':
        print(f'erro >> mesa {n} desocupada')
    elif i not in cardapio:
        print(f'erro >> item {i} nao existe no cardapio')
    elif tem_suf(i, cardapio, estoque):
        print(f'erro >> ingredientes insuficientes para produzir o item {i}')
    else:
        for elemento in cardapio[i]:
            estoque[elemento] -= cardapio[i][elemento]
            if estoque[elemento] == 0:
                estoque.pop(elemento)
        
        if n in pedidos:
            pedidos[n].append(i)
        else:
            pedidos[n] = [i]
            
        pedidos_tempo.append((n, i))
        
        print(f'sucesso >> pedido realizado: item {i} para mesa {n}')
        
def relatorio_pedidos(pedidos):
    if len(pedidos) != 0:
        pedidos_order = sorted(pedidos)
        for elemento in pedidos_order:
            print(f'mesa: {elemento}')
            pratos_order = sorted(pedidos[elemento])
            for item in pratos_order:
                print(f'- {item}')
    else:
        print('- nenhum pedido foi realizado')
        
def fechar_restaurante(pedidos_tempo):
    if len(pedidos_tempo) != 0:
        for i in range(len(pedidos_tempo)):
            print(f'{i + 1}. mesa {pedidos_tempo[i][0]} pediu {pedidos_tempo[i][1]}')
    else:
        print('- historico vazio')
              

#####################################################################################################
######################################## main function ##############################################
#####################################################################################################

mesas_area = {}
mesas_status = {}
cardapio = {}
estoque = {}
pedidos = {}
pedidos_tempo = []
areas = []

print('=> restaurante aberto')

while True:
    comando = input()
    if comando == '+ atualizar mesas':
        atualiza_mesas(mesas_area, mesas_status, areas)
    elif comando == '+ atualizar cardapio':
        atualiza_cardapio(cardapio)
    elif comando == '+ atualizar estoque':
        atualiza_estoque(estoque)
    elif comando == '+ relatorio mesas':
        relatorio_mesas(mesas_area, mesas_status, areas)
    elif comando == '+ relatorio cardapio':
        relatorio_cardapio(cardapio)
    elif comando == '+ relatorio estoque':
        relatorio_estoque(estoque)
    elif comando == '+ fazer pedido':
        fazer_pedido(mesas_status, cardapio, estoque, pedidos, pedidos_tempo)
    elif comando == '+ relatorio pedidos':
        relatorio_pedidos(pedidos)
    elif comando == '+ fechar restaurante':
        fechar_restaurante(pedidos_tempo)
        print('=> restaurante fechado')
        break
    else:
        print('erro >> comando inexistente')