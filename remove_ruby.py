# 青空文庫のテキストを整形する
# 1. ルビを削除する
# 2. ヘッダーを削除する
# 3. フッターを削除する
# 4. 脚注を削除する
# 5. 空行を削除する

import sys
import re
import glob
import os

def file_open(filename):
    with open(filename, "r", encoding="shift_jis") as f:
        lines = f.readlines()
    return lines

def file_write(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(lines)

def remove_ruby(lines):
    # ルビを削除する
    # ルビの例
    # ｜吾輩《わがはい》は猫である
    # 吾輩は猫《ねこ》である

    # ｜はそのまま削除する
    # 《》の中身を削除する

    return_lines = []
    for line in lines:
        # ｜を削除する
        line = line.replace("｜", "")
        # 《》の中身を削除する
        line = re.sub("《.+?》", "", line)
        return_lines.append(line)
    return return_lines

def remove_header(lines):
    # ヘッダーを削除する
    # ヘッダーの例
    # -------------------------------------------------------
    # 【テキスト中に現れる記号について】
    # 
    # 《》：ルビ
    # （例）お葉《えふ》
    # -------------------------------------------------------

    # ヘッダーの開始行を探す
    header_start = 0
    for i, line in enumerate(lines):
        if line.startswith("-------------------------------------------------------"):
            header_start = i
            break
    # ヘッダーの終了行を探す
    header_end = 0
    for i, line in enumerate(lines[header_start+1:]):
        if line.startswith("-------------------------------------------------------"):
            header_end = i
            break
    # ヘッダーを削除する
    return lines[:header_start] + lines[header_start+header_end+2:]

def remove_footer(lines):
    # フッターを削除する
    # フッターの例
    # 底本：「現代日本文學全集　85　大正小説集」筑摩書房
    #　　　1957（昭和32）年12月20日発行
    # 入力：小林徹
    # 校正：野口英司
    # ......

    # 底本：から始まる行を探す
    # 偶然　底本：という文字列が本文中に出てきたら諦める
    footer_start = 0
    for i, line in enumerate(lines):
        if line.startswith("底本："):
            footer_start = i
            break

    # フッターを削除する
    return lines[:footer_start]

def remove_footnote(lines):
    # 脚注を削除する
    # 脚注の例
    # ［＃「麾」の「毛」にかえて「公」の右上の欠けたもの、第4水準2-94-57］

    # 脚注の正規表現
    pattern = r"［＃.+?］"

    return_lines = []
    for line in lines:
        # 脚注を削除する
        line = re.sub(pattern, "", line)
        return_lines.append(line)
    return return_lines

def remove_empty_line(lines):
    # 空行を削除する
    return_lines = []
    for line in lines:
        # 空行を削除する
        if line == "\n":
            continue
        return_lines.append(line)
    return return_lines

def main():
    # ファイル名を取得する
    dirname = sys.argv[1]
    # 指定されたフォルダ以下で、_ruby_removed.txtでないファイルを取得する
    filenames = glob.glob(os.path.join(dirname, "**", "*.txt"), recursive=True)
    filenames = [filename for filename in filenames if not filename.endswith("_ruby_removed.txt")]
    not_ruby_removed_filenames = []
    # ファイルごとに処理する
    for filename in filenames:
        # エラーが出たものはスキップする
        try:
            print(filename)
            # ファイルを開く
            lines = file_open(filename)
            # ルビを削除する
            lines = remove_ruby(lines)
            # ヘッダーを削除する
            lines = remove_header(lines)
            # フッターを削除する
            lines = remove_footer(lines)
            # 脚注を削除する
            lines = remove_footnote(lines)
            # 空行を削除する
            lines = remove_empty_line(lines)
            # ファイルを保存する
            file_write(filename.replace(".txt", "_ruby_removed.txt"), lines)
        except:
            not_ruby_removed_filenames.append(filename)

    # エラーが出たファイルを記録する
    with open("not_ruby_removed_filenames.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(not_ruby_removed_filenames))
        
    
if __name__ == "__main__":
    main()