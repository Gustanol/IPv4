import ipaddress as ip
import math
from pathlib import Path as path
import datetime
def ipv4(x): # Conversão em IPv4
  return ip.ip_address(x)
def subnet(x): # Conversão em comprimento do prefixo
  network = ip.ip_network(f'0.0.0.0/{x}', strict=False)
  return network.prefixlen
def cidr(x, y): # Conversão para formato de rede (CIDR)
  return ip.ip_network(f'{x}/{y}', strict=False)
def two_expo(x): # Validação de potência de dois
  if x > 0 and (x & (x - 1)) == 0:
    return True
  else:
    return False
def two_expo2(y): # Conversâo de um número para a potência de dois acima dele
  x = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32)
  for a, b in enumerate(x):
    if 2**b >= y+2:
      return 2**b
def two_expo2a(y):
  x = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32)
  for a, b in enumerate(x):
    if 2**b >= y:
      return b
def two_expo3(y):
  x = math.log2(y)
  return x
def vlsm(a, b, c, d, e, g):
  # a = values1; b = values2; c = subnet2.netmask; d = x; e = y; f = txt_file
  print(f'\nSub-rede {d+1}: {b[d]}/{e} ({b[d]+1} - {b[d+1]-2})')
  print(f'Endereço de broadcast: {b[d+1]-1}')
  print(f'Máscara de sub-rede: {c}')
  print(f'Número de endereços: {a[d]}')
  print(f'Número de hosts: {a[d]-2}\n')
  with open(g, 'a') as f:
    f.write(f'\nSub-rede {d+1}: {b[d]}/{e} ({b[d]+1} - {b[d+1]-2})\n')
    f.write(f'Endereço de broadcast: {b[d+1]-1}\n')
    f.write(f'Máscara de sub-rede: {c}\n')
    f.write(f'Número de endereços: {a[d]}\n')
    f.write(f'Número de hosts: {a[d]-2}\n')
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
timestamp2 = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
dirc = path('Python/IPv4/Files') # Criação de pastas
dirc.mkdir(parents=True, exist_ok=True)
txt_file = dirc / f'subredes_{timestamp}.txt'
a = False
b = True
a1 = False
a2 = True
a3 = True
network = cidr('10.0.0.0', '8') # Primeira faixa de endereços privados
network1 = cidr('172.16.0.0', '12') # Segunda faixa de endereços privados
network2 = cidr('192.168.0.0', '16') # Terceira faixa de endereços privados
print("Calculadora de sub-rede IPv4!\n")
while not a:
  adr = input("Digite o endereço da rede IPv4: ") # Captura do endereço da rede
  try:
    ipv4_1 = ipv4(adr)
    if ipv4_1.is_private:
      a = True
    else:
      print(f'\nDigite um endereço privado!\n\nFaixa de endereços privados:\n{network}\n{network1}\n{network2}\n')
  except ip.AddressValueError:
    print("Endereço IP inválido!")
while a:
  s = input("Digite a máscara de sub-rede ou o comprimento do prefixo: ") # Captura da máscara de sub-rede
  try: # Validação da máscara de sub-rede
    sn = subnet(s)
    if ipv4_1 in network and 8 < sn <= 30:
      a = False
    elif ipv4_1 in network1 and 12 < sn <= 30:
      a = False
    elif ipv4_1 in network2 and 16 < sn <= 30:
      a = False
    elif (ipv4_1 in network and sn == network.prefixlen) or (ipv4_1 in network1 and sn == network1.prefixlen) or (ipv4_1 in network2 and sn == network2.prefixlen):
      print('\nDigite uma máscara de sub-rede diferente da original!\n')
    else:
      print("\nDigite uma máscara de sub-rede dentro do intervalo da sua rede!\n")
  except ip.AddressValueError:
    print("Máscara de sub-rede inválida!")
ip_cidr = cidr(ipv4_1, sn)
values = [] # Quantidade de hosts
values1 = [] # Conversão da quantidade de hosts para potências de dois
values2 = [] # Endereços IP para cada sub-rede
values3 = [] # Comprimento do prefixo para cada sub-rede
values2.append(ipv4_1)
address = 2**(32 - sn)
address_1 = address
print(f'\nEndereço da rede: {ip_cidr}')
print(f'Máscara de sub-rede: {ip_cidr.netmask}')
print(f'Endereço de Broadcast: {ip_cidr.broadcast_address}')
print(f'Número de endereços: {address}\n')
while not a1:
  c = str(input('Deseja segmentar a rede em sub-redes de tamanhos variados? [Y/N]: '))
  if c.lower() == "y": # VLSM
    a1 = True
    for i in range(int(math.sqrt(address))):
      while a1:
        sb = int(input(f'\nDigite a quantidade de hosts para a {i+1}° sub-rede: '))
        values.append(sb)
        z = two_expo2(values[i])
        if z > address:
          print("Digite um número menor!")
          values.pop()
        elif z == address_1:
          print("Digite um valor menor do que a quantidade total de endereços!")
          values.pop()
        else:
          a1 = False
          values1.append(z)
          address -= z
          ipv4_1 = int(ipv4_1) + values1[i]
          values2.append(ipv4(ipv4_1))
          z1 = two_expo3(values1[i])
          sn1 = (32 - sn) - z1
          sn2 = int(sn + sn1)
          values3.append(sn2)
          print(f'\nQuantidade de endereços restantes: {address}')
          a = False
      while not a:
        e = str(input('Deseja continuar? [Y/N]: '))
        if e.lower() == 'y':
          a1 = True
          a = True
        elif e.lower() == 'n':
          a1 = True
          a = True
          b = False
          print(f'\nRede principal: {ip_cidr}')
          with open(txt_file, 'a') as f:
            f.write(f'Rede principal: {ip_cidr}\n')
          for x, y in enumerate(values3):
            subnet2 = cidr('0.0.0.0', y)
            vlsm(values1, values2, subnet2.netmask, x, y, txt_file)
          with open(txt_file, 'a') as f:
            f.write(f'\n\nArquivo gerado em: {timestamp2}\n')
          print("Arquivo criado com sucesso!\n")
          print("Procure pela pasta 'Python' na raiz do armazenamento para ver o relatório!")
        else:
          a = False
          print("Digite 'Y' ou 'N'! ")
      if a and not b:
        break
  elif c.lower() == "n":
    a1 = True
    while a2:
      sb1 = input("\nDigite a quantidade de sub-redes necessárias: ")
      try:
        print('\n')
        sb1 = int(sb1)
        q_subnet = two_expo2a(sb1)
        sn_no_vlsm = sn+q_subnet
        cidr_no_vlsm = cidr('0.0.0.0', sn_no_vlsm)
        if 2**q_subnet < address_1 and sn_no_vlsm <= 30:
          a2 = False
          no_vlsm = ip_cidr.subnets(new_prefix=sn_no_vlsm)
          print(f'Nova máscara de sub-rede: {cidr_no_vlsm.netmask}')
          print(f'Número de endereços em cada sub-rede: {2**(32-sn_no_vlsm)}')
          print(f'Número de hosts em cada sub-rede: {2**(32-sn_no_vlsm)-2}\n')
          with open(txt_file, 'a') as f1:
            f1.write(f'Nova máscara de sub-rede: {cidr_no_vlsm.netmask}\n')
            f1.write(f'Número de endereços em cada sub-rede: {2**(32-sn_no_vlsm)}\n')
            f1.write(f'Número de hosts em cada sub-rede: {2**(32-sn_no_vlsm)-2}\n\n')
          for a, b in enumerate(no_vlsm):
            print(f'Sub-rede {a+1}: {b}')
            print(f'Endereço de broadcast: {b.broadcast_address}\n')
            with open(txt_file, 'a') as f1:
              f1.write(f'Sub-rede {a+1}: {b}\n')
              f1.write(f'Endereço de broadcast: {b.broadcast_address}\n\n')
          with open(txt_file, 'a') as f1:
            f1.write(f'\nArquivo gerado em: {timestamp2}\n')
          print("Arquivo criado com sucesso!\n")
          print("Procure pela pasta 'Python' na raiz do armazenamento para ver o relatório!")
        else:
          print('Essa rede não suporta esta quantidade de sub-redes!')
      except ValueError:
        print("\nDigite um valor numérico!")
  else:
    print("Digite 'Y' ou 'N'!")