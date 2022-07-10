import random
from secrets import choice
import numpy as np
import os, os.path
import json
from PIL import Image
import ipfs

def generate_json(dir_name, foldername):
    json_file = open("../jsons/"+foldername+".json", "w")
    json_file.write("{")
    for file in os.listdir(dir_name):
        if (file != os.listdir(dir_name)[-1]):
            json_file.write('\"'+file.split('.')[0]+'\":{ "name":\"'+file+'\", "path":\"'+(dir_name+"/"+file)+'\", "prob":\"'+str(100)+'\" },')
        else: 
            json_file.write('\"'+file.split('.')[0]+'\":{ "name":\"'+file+'\", "path":\"'+(dir_name+"/"+file)+'\", "prob":\"'+str(100)+'\" }')
    json_file.write("}")
    json_file.close()

def generate_all_jsons():
    dir = "../layers"
    for folder in os.listdir(dir):
        fpath = dir+"/"+folder
        if os.path.isdir(fpath):
            generate_json(str(fpath), folder)

def generate_nft_dna(count):
    layers_arr = []
    layers_components = []

    dir = "../jsons"
    for jsonfile in os.listdir(dir):
        print((dir+"/"+jsonfile))
        file = open((dir+"/"+jsonfile), "r")
        json_object = json.loads(file.read())
        file.close()
        arr = []
        for key in json_object:
            arr.append(key)
        layers_arr.append(arr)
        layers_components.append(json_object)

    file = open("../nft_dna/dna.txt", "w")

    for i in range(count):
        dna_str = ""
        for i in range(len(layers_arr)):
            if len(layers_arr[i]) != 0:
                if i != 0:
                    dna_str += ('-'+str(i)+'-')
                else:
                    dna_str += (str(i)+'-')
                print(layers_arr[i])
                dna = random.choice(layers_arr[i])
                chance = random.randint(1,100)
                while int(layers_components[i][dna]['prob']) < chance:
                    print("probability failed")
                    print("item: {0}".format(dna))
                    print("chance: {0}".format(chance))
                    dna = random.choice(layers_arr[i])
                    chance = random.randint(1,100)
                dna_str += dna
    
        if (i == count-1):
            file.write(dna_str)
        else:
            file.write(dna_str+",")
    file.close()

def build_nfts(dna_path, policy_id, project_name):
    
    layers_arr = []
    dir = "../jsons"
    for jsonfile in os.listdir(dir):
        file = open(os.path.join(dir, jsonfile), "r")
        json_layers = json.loads(file.read())
        file.close()
        arr = []
        for key in json_layers:
            arr.append(json_layers[key])
        layers_arr.append(json_layers)

    dna_file = open(dna_path, "r")

    dna_content = dna_file.read()
    dna_arr = dna_content.split(",")
    key = None

    count = 1
    for dna in dna_arr:
        components = []
        print(dna)
        if (dna != ""):
            dna_components = dna.split("-")
            hbc = Image.open("../layers/layer0/background_1.png")
            for i in dna_components:
                if i.isdigit():
                    key = int(i)
                    continue
                if key != None:
                    components.append(i)
                    layer = Image.open((layers_arr[key])[i]['path']).convert("RGBA")
                    hbc.paste(layer, (0,0), layer)
                    key = None
            hbc.save("../output/{0}{1}.png".format(project_name, str(count)), "PNG")
            build_metadata(policy_id, project_name, "{0}{1}".format(project_name, str(count)), components)
            count = count + 1

def build_metadata(policy_id, project_name, token_name, layers):
    template = open("../config/metadata_template.json", 'r')
    content = template.read()
    template.close()
    content = content.replace('{$policy}', policy_id)
    content =content.replace('{$token}', project_name)
    content = content.replace('{$name}', token_name)
    for i in range(len(layers)):
        content = content.replace("$layer{0}".format(str(i)), layers[i])
    
    metadata_json = open("../output/metadata/{0}.json".format(token_name), 'w')
    metadata_json.write(content)
    metadata_json.close()


def upload():
    dir = "../output"
    for nft in os.listdir(dir):
        print(dir+"/"+nft)
        if os.path.isfile(dir+"/"+nft):
            print("file")
            print(dir+"/"+nft)
            cid = ipfs.upload_image(dir+"/"+nft)['ipfs_hash']
            print(cid)
            metafile = "../output/metadata/{0}.json".format(nft.split('.')[0])

            meta_json= open(metafile, 'r')
            metadata = meta_json.read()
            meta_json.close()
            
            meta_json= open(metafile, 'w')
            metadata = metadata.replace('{$CID}', cid)
            meta_json.write(metadata)
            meta_json.close()

generate_all_jsons()
generate_nft_dna(10)
build_nfts("../nft_dna/dna.txt", "POLICY ID", "PROJECT NAME")

# Uncomment if you want to upload to blockfrost ipfs...
#upload()