#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Desinstalador da Traducao 100% PT-BR de Just Cause (2006)
Restaura os arquivos originais do jogo.
"""

import sys
import os
import argparse

ORIGINAL_PC4_SIZE = 71047168

def find_game_archives_dir(user_path=None):
    if user_path:
        cand = os.path.abspath(user_path)
        if os.path.isdir(cand):
            if os.path.exists(os.path.join(cand, "pc.tab")):
                return cand
            if os.path.exists(os.path.join(cand, "Archives", "pc.tab")):
                return os.path.join(cand, "Archives")

    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "pc.tab")):
        return cwd
    if os.path.exists(os.path.join(cwd, "Archives", "pc.tab")):
        return os.path.join(cwd, "Archives")

    common_locations = [
        os.path.expanduser("~/.local/share/Steam/steamapps/common/Just Cause/Archives"),
        os.path.expanduser("~/.steam/steam/steamapps/common/Just Cause/Archives"),
        os.path.expanduser("~/.steam/root/steamapps/common/Just Cause/Archives"),
        "/run/media/nta/Games/SteamLibrary/steamapps/common/Just Cause/Archives",
        r"C:\Program Files (x86)\Steam\steamapps\common\Just Cause\Archives",
        r"C:\Program Files\Steam\steamapps\common\Just Cause\Archives",
        r"D:\SteamLibrary\steamapps\common\Just Cause\Archives",
        r"E:\SteamLibrary\steamapps\common\Just Cause\Archives",
        r"F:\SteamLibrary\steamapps\common\Just Cause\Archives",
        r"C:\GOG Games\Just Cause\Archives",
        r"D:\GOG Games\Just Cause\Archives",
    ]

    for loc in common_locations:
        if os.path.exists(os.path.join(loc, "pc.tab")):
            return loc

    return None

def main():
    print("=" * 65)
    print("   JUST CAUSE (2006) - DESINSTALADOR DA TRADUCAO PT-BR")
    print("=" * 65)

    parser = argparse.ArgumentParser(description="Desinstalador da Traducao de Just Cause 1")
    parser.add_argument("--game-dir", help="Caminho para a pasta do jogo Just Cause ou a pasta Archives")
    args = parser.parse_args()

    archives_dir = find_game_archives_dir(args.game_dir)

    while not archives_dir:
        typed = input("Digite o caminho da pasta onde o Just Cause esta instalado: ").strip()
        if not typed:
            print("Desinstalacao cancelada.")
            sys.exit(1)
        archives_dir = find_game_archives_dir(typed)

    pc_tab_path = os.path.join(archives_dir, "pc.tab")
    pc_tab_orig = os.path.join(archives_dir, "pc.tab.orig")
    pc4_arc_path = os.path.join(archives_dir, "pc4.arc")

    if not os.path.exists(pc_tab_orig):
        print(f"ERRO: Nao foi encontrado o arquivo de backup original: {pc_tab_orig}")
        print("Caso tenha verificado a integridade dos arquivos pela Steam, o jogo ja esta no estado original.")
        sys.exit(1)

    print("\nRestaurando o arquivo de indice original (pc.tab)...")
    with open(pc_tab_orig, "rb") as f_in, open(pc_tab_path, "wb") as f_out:
        f_out.write(f_in.read())

    print("Restaurando pc4.arc para o tamanho original...")
    with open(pc4_arc_path, "r+b") as f:
        f.truncate(ORIGINAL_PC4_SIZE)

    print("\n" + "=" * 65)
    print("   DESINSTALACAO CONCLUIDA! JOGO RESTAURADO AO ESTADO ORIGINAL!")
    print("=" * 65)

if __name__ == "__main__":
    main()
