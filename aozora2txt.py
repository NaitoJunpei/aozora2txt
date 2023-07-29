import os
import glob
import zipfile

# 特定のフォルダ以下の全てのサブフォルダについて、zipファイルをコピーする
aozora_dir = os.path.join("F:", "private", "llm", "string_dataset", "aozorabunko", "cards")
print(os.path.exists(aozora_dir))
target_dir = os.path.join("F:", "private", "llm", "string_dataset", "aozorabunko", "all_zip")
zip_filenames = glob.glob(os.path.join(aozora_dir, "*", "*", "*.zip"))

#for zip_filename in zip_filenames :
#    os.system("copy {} {}".format(zip_filename, target_dir))

# zipファイルを解凍する
zip_filenames = glob.glob(os.path.join(target_dir, "*.zip"))
for zip_filename in zip_filenames :
    print(zip_filename)
    with zipfile.ZipFile(zip_filename) as zip_file :
        zip_file.extractall(os.path.join(target_dir, os.path.basename(zip_filename).replace(".zip", "")))
    os.remove(zip_filename)