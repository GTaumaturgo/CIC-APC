#  -*- coding: utf-8 -*-
#    @package: 03-mp3.py
#     @author: Guilherme N. Ramos (gnramos@unb.br)
# @disciplina: Algoritmos e Programação de Computadores
#
# Exemplo de uso de registro (ID3v1) para armazenar as
# informações de um arquivo no formato MP3. Veja mais em:
# http://en.wikipedia.org/wiki/ID3#ID3v1


from subprocess import check_call
import sys


class mp3_ID3v1():
    def __init__(self):
        self.header = ''
        self.titulo = ''
        self.artista = ''
        self.album = ''
        self.ano = ''
        self.comentario = ''
        self.genero = ''


def existe_e_pode_abrir(arquivo):
    '''Indica se é possível abrir o arquivo para leitura.'''
    try:
        with open(arquivo, 'rb'):
            pass
        return True
    except:
        return False


def valido(id3v1):
    '''Indica se o registro está preenchido corretamente.'''
    return id3v1.header == 'TAG'


def binario_em_ascii(bytes):
    '''Retorna a representação em ASCII de um string binário.'''
    return ''.join(chr(b) for b in bytes)


def le_ID3v1(arquivo):
    '''Tenta abrir e ler o arquivo MP3 para preencher um registro com as
    informações (supõe que o arquivo existe). Retorna o registro preenchido, se
    conseguiu abrir, vazio caso contrário.'''
    id3v1 = mp3_ID3v1()

    try:
        with open(arquivo, 'rb') as f:
            f.seek(-128, 2)

            id3v1.header = binario_em_ascii(f.read(3))
            id3v1.titulo = binario_em_ascii(f.read(30))
            id3v1.artista = binario_em_ascii(f.read(30))
            id3v1.album = binario_em_ascii(f.read(30))
            id3v1.ano = binario_em_ascii(f.read(4))
            id3v1.comentario = binario_em_ascii(f.read(30))
            id3v1.genero = ord(f.read(1))
    except:
        print('Erro ao tentar abrir %s.\n' % arquivo)

    return id3v1


def mostra_ID3v1(id3v1):
    '''Exibe as informações do registro na saída padrão.'''
    print('Título:', id3v1.titulo)
    print('Artista:', id3v1.artista)
    print('Album:', id3v1.album)
    print('Ano:', id3v1.ano)

    if id3v1.comentario[28] == '\0':
        print('Comentário: %.28s' % id3v1.comentario)
        print('Número: %d' % ord(id3v1.comentario[29]))
    else:
        print('Comentário:', id3v1.comentario)

    print('Gênero:', str(id3v1.genero))


def quer_abrir_com(aplicativo):
    '''Indica se o usuário deseja abrir o arquivo com o programa.'''
    resposta = input('Abrir o arquivo com o aplicativo \'' + aplicativo + '\'? (S/N) ')

    return resposta in 'sS'


def abre(arquivo, aplicativo):
    '''Tenta abrir o arquivo dado com o aplicativo dado, retornando o resultado
    da chamada.'''
    cmd = aplicativo + ' \'' + arquivo + '\''
    return check_call(cmd, shell=True)


if __name__ == '__main__':
    aplicativo = ''

    # Validação da entrada.
    argc = len(sys.argv)
    if(argc < 2):
        print('É preciso passar pelo menos um arquivo MP3 como argumento.')
        exit(1)
    elif(argc > 2):
        aplicativo = sys.argv[2]

    # Verificação da entrada.
    arquivo = sys.argv[1]
    if not existe_e_pode_abrir(arquivo):
        print('Arquivo \'%s\' não encontrado ou não pode ser lido.\n' % arquivo)
        exit(1)

    # Leitura do cabeçalho.
    id3v1 = le_ID3v1(arquivo)
    if not valido(id3v1):
        print('Não foi possível ler cabeçalho arquivo \'%s\'.\n' % arquivo)
        exit(1)

    mostra_ID3v1(id3v1)

    # "Bônus"
    if aplicativo and quer_abrir_com(aplicativo):
        if abre(arquivo, aplicativo):
            print('Erro ao tentar abrir o arquivo \'%s\' com o aplicativo \'%s\'.\n' % (arquivo, aplicativo))
