#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador da Traducao 100% PT-BR para Just Cause (2006)
Compativel com Windows e Linux (Steam / GOG / DVD).
Sem dependencias externas - requer apenas Python 3.6+.
"""

import sys
import os
import struct
import json
import csv
import io
import unicodedata
import argparse

ORIGINAL_PC4_SIZE = 71047168
ALIGN = 2048

def remove_accents(input_str):
    replacements = {
        "ç": "c", "Ç": "C",
        "ã": "a", "Ã": "A",
        "õ": "o", "Õ": "O",
        "á": "a", "Á": "A",
        "à": "a", "À": "A",
        "â": "a", "Â": "A",
        "é": "e", "É": "E",
        "ê": "e", "Ê": "E",
        "í": "i", "Í": "I",
        "ó": "o", "Ó": "O",
        "ô": "o", "Ô": "O",
        "ú": "u", "Ú": "U",
        "ü": "u", "Ü": "U",
    }
    for k, v in replacements.items():
        input_str = input_str.replace(k, v)
    nfkd = unicodedata.normalize("NFKD", input_str)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def find_game_archives_dir(user_path=None):
    if user_path:
        cand = os.path.abspath(user_path)
        if os.path.isdir(cand):
            if os.path.exists(os.path.join(cand, "pc.tab")):
                return cand
            if os.path.exists(os.path.join(cand, "Archives", "pc.tab")):
                return os.path.join(cand, "Archives")

    # Verificar pasta atual e subpastas
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "pc.tab")):
        return cwd
    if os.path.exists(os.path.join(cwd, "Archives", "pc.tab")):
        return os.path.join(cwd, "Archives")

    # Locais padrao comuns no Windows e Linux
    common_locations = [
        # Linux
        os.path.expanduser("~/.local/share/Steam/steamapps/common/Just Cause/Archives"),
        os.path.expanduser("~/.steam/steam/steamapps/common/Just Cause/Archives"),
        os.path.expanduser("~/.steam/root/steamapps/common/Just Cause/Archives"),
        "/run/media/nta/Games/SteamLibrary/steamapps/common/Just Cause/Archives",
        # Windows
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

def patch_csv_data(csv_bytes, ptbr_map):
    if b"#D#" in csv_bytes:
        lines = csv_bytes.split(b"\r\n")
        delim = b"\r\n" if len(lines) > 1 or csv_bytes.endswith(b"\r\n") else b"\n"
        if delim == b"\n":
            lines = csv_bytes.split(b"\n")
        rep = 0
        new_lines = []
        for l in lines:
            if not l.strip():
                new_lines.append(l)
                continue
            cols = l.split(b"#D#")
            if len(cols) >= 4:
                k = cols[1].decode("latin1", errors="replace")
                if k in ptbr_map:
                    pt = ptbr_map[k].encode("utf-8")
                    for c_idx in (3, 5, 7, 9, 11, 13, 15):
                        if c_idx < len(cols):
                            cols[c_idx] = pt
                    rep += 1
            new_lines.append(b"#D#".join(cols))
        return delim.join(new_lines), rep
    else:
        text = csv_bytes.decode("utf-8", errors="replace")
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        rep = 0
        out = io.StringIO()
        writer = csv.writer(out, lineterminator="\r\n")
        for r in rows:
            if r and r[0] in ptbr_map:
                pt = ptbr_map[r[0]]
                for col_idx in range(1, len(r)):
                    r[col_idx] = pt
                rep += 1
            writer.writerow(r)
        return out.getvalue().encode("utf-8"), rep

def rebuild_sarc(data, ptbr_map):
    v, magic, flag, val12 = struct.unpack("<I4s2I", data[:16])
    nlen = struct.unpack("<I", data[16:20])[0]
    first_off = struct.unpack("<I", data[20 + nlen : 24 + nlen])[0]
    
    p = 16
    files = []
    while p + 8 <= first_off:
        nl = struct.unpack("<I", data[p:p+4])[0]
        if nl == 0 or p + 4 + nl + 8 > first_off: break
        p += 4
        nm = data[p:p+nl]
        p += nl
        off, fsz = struct.unpack("<2I", data[p:p+8])
        p += 8
        files.append((nm, off, fsz, data[off:off+fsz]))
    
    total_rep = 0
    patched_files = []
    for nm, old_off, old_sz, f_data in files:
        nm_str = nm.decode("latin1", errors="replace")
        if nm_str.lower().endswith(".csv"):
            new_csv, rep = patch_csv_data(f_data, ptbr_map)
            total_rep += rep
            patched_files.append((nm, new_csv))
        else:
            patched_files.append((nm, f_data))
    
    new_dir = bytearray()
    new_data = bytearray()
    cur_off = first_off
    for nm, f_data in patched_files:
        new_dir.extend(struct.pack("<I", len(nm)))
        new_dir.extend(nm)
        new_dir.extend(struct.pack("<2I", cur_off, len(f_data)))
        new_data.extend(f_data)
        cur_off += len(f_data)
    
    pad_len = (first_off - 16) - len(new_dir)
    assert pad_len >= 0, f"Erro: cabecalho expandiu inesperadamente {-pad_len} bytes"
    new_dir.extend(b"\x00" * pad_len)
    
    return data[:16] + new_dir + new_data, total_rep

def main():
    print("=" * 65)
    print("   JUST CAUSE (2006) - INSTALADOR DA TRADUCAO 100% PT-BR")
    print("=" * 65)

    parser = argparse.ArgumentParser(description="Instalador da Traducao de Just Cause 1 para PT-BR")
    parser.add_argument("--game-dir", help="Caminho para a pasta do jogo Just Cause ou a pasta Archives")
    args = parser.parse_args()

    # Localizar dicionario de traducao
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "translations_ptbr.json")
    if not os.path.exists(json_path):
        print(f"ERRO: Nao foi encontrado o arquivo de traducao: {json_path}")
        sys.exit(1)

    print("\n[1/4] Carregando dicionario de traducao...")
    with open(json_path, "r", encoding="utf-8") as f:
        raw_map = json.load(f)
    ptbr_map = {k: remove_accents(v) for k, v in raw_map.items()}
    print(f"      -> {len(ptbr_map)} textos carregados com sucesso!")

    # Localizar pasta Archives
    print("\n[2/4] Localizando instalacao do jogo...")
    archives_dir = find_game_archives_dir(args.game_dir)

    while not archives_dir:
        print("\nNao foi possivel detectar a pasta do jogo automaticamente.")
        typed = input("Digite o caminho da pasta onde o Just Cause esta instalado: ").strip()
        if not typed:
            print("Instalacao cancelada.")
            sys.exit(1)
        archives_dir = find_game_archives_dir(typed)

    print(f"      -> Pasta do jogo localizada: {archives_dir}")

    pc_tab_path = os.path.join(archives_dir, "pc.tab")
    pc_tab_orig = os.path.join(archives_dir, "pc.tab.orig")
    pc4_arc_path = os.path.join(archives_dir, "pc4.arc")

    if not os.path.exists(pc_tab_path) or not os.path.exists(pc4_arc_path):
        print("ERRO: Os arquivos 'pc.tab' ou 'pc4.arc' nao foram encontrados na pasta informada.")
        sys.exit(1)

    # Backup do arquivo de indice
    print("\n[3/4] Verificando backups...")
    if not os.path.exists(pc_tab_orig):
        print("      Criando backup original (pc.tab.orig)...")
        with open(pc_tab_path, "rb") as f_in, open(pc_tab_orig, "wb") as f_out:
            f_out.write(f_in.read())
        print("      -> Backup criado com sucesso!")
    else:
        print("      -> Backup original existente detectado.")

    # Reset do pc4.arc para tamanho base
    with open(pc4_arc_path, "r+b") as f:
        f.truncate(ORIGINAL_PC4_SIZE)

    # Iniciar processo de injecao
    print("\n[4/4] Injetando traducao nos arquivos do jogo...")

    with open(pc_tab_orig, "rb") as f:
        tab_bytes = bytearray(f.read())

    ver, align, num_arcs = struct.unpack("<3I", tab_bytes[:12])
    arc_sizes = [os.path.getsize(os.path.join(archives_dir, f"pc{i}.arc")) for i in range(num_arcs)]
    arc_files = [open(os.path.join(archives_dir, f"pc{i}.arc"), "rb") for i in range(num_arcs)]

    def read_entry(block, size):
        total_byte_offset = block * align
        local_offset = total_byte_offset
        arc_idx = 0
        for i, s in enumerate(arc_sizes):
            if local_offset < s:
                arc_idx = i
                break
            local_offset -= s
        f = arc_files[arc_idx]
        f.seek(local_offset)
        return f.read(size)

    base_pc4_offset = sum(arc_sizes[:4])
    current_pc4_size = ORIGINAL_PC4_SIZE

    out_arc = open(pc4_arc_path, "r+b")
    out_arc.seek(0, os.SEEK_END)

    num_entries = (len(tab_bytes) - 12) // 12
    sarcs_patched = 0
    total_keys = 0

    for i in range(num_entries):
        h, block, sz = struct.unpack("<3I", tab_bytes[12 + i*12 : 12 + (i+1)*12])
        head = read_entry(block, min(sz, 64))

        # Arquivo de controles de teclado
        if i == 731:
            data = read_entry(block, sz)
            patched_data, rep = patch_csv_data(data, ptbr_map)
            pad = (ALIGN - (current_pc4_size % ALIGN)) % ALIGN
            if pad > 0:
                out_arc.write(b"\x00" * pad)
                current_pc4_size += pad
            new_block = (base_pc4_offset + current_pc4_size) // ALIGN
            new_size = len(patched_data)
            out_arc.write(patched_data)
            current_pc4_size += new_size
            struct.pack_into("<2I", tab_bytes, 12 + i*12 + 4, new_block, new_size)
            total_keys += rep
            continue

        # Conteineres SARC com arquivos de texto CSV
        if head.startswith(b"\x04\x00\x00\x00SARC") and b".csv" in read_entry(block, min(sz, 1024)):
            data = read_entry(block, sz)
            rebuilt_sarc, rep = rebuild_sarc(data, ptbr_map)
            if rep > 0:
                pad = (ALIGN - (current_pc4_size % ALIGN)) % ALIGN
                if pad > 0:
                    out_arc.write(b"\x00" * pad)
                    current_pc4_size += pad
                new_block = (base_pc4_offset + current_pc4_size) // ALIGN
                new_size = len(rebuilt_sarc)
                out_arc.write(rebuilt_sarc)
                current_pc4_size += new_size
                struct.pack_into("<2I", tab_bytes, 12 + i*12 + 4, new_block, new_size)
                total_keys += rep
                sarcs_patched += 1

    out_arc.flush()
    out_arc.close()
    for f in arc_files:
        f.close()

    # Gravar indice pc.tab atualizado
    with open(pc_tab_path, "wb") as f:
        f.write(tab_bytes)

    print("\n" + "=" * 65)
    print("   TRADUCAO INSTALADA COM SUCESSO! 100% PRONTO!")
    print("=" * 65)
    print(f" -> Conteineres modificados: {sarcs_patched}")
    print(f" -> Linhas traduzidas injetadas: {total_keys}")
    print("\nVoce ja pode abrir o jogo pela Steam! Bom jogo!")

if __name__ == "__main__":
    main()
