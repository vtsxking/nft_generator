# NFT Random Generator
 
## Description
Combines multiple layer randomly into a single image, pins to IPFS, and creates metadata json. Simply place your layers in the different layer folders in the proper layer ordering and run `nft_generator.py` script. The script with then scan all the layers and creates jsons with all the required data for use later. After scanning the script will then create a random string of chars and file names in the `dna.txt` this it to regenerate the same nfts later if need but will also be used to create the inital images. Once `dna.txt` is created the script with read that file and the layer jsons and merge a all the layer in the order they are given.

## Usage
Place your layers in the corresponding folders, on line `134 generate_nft_dna(10)` change the 10 to any number n greater than 0 to generate n nfts and metadata jsons.

if you wish to also use blockfrost to host the images on in the `ipfs.py` file replace line `5 api_key = "api key here"` with your own api key and uncomment `138 #upload()`.
if by anychance you need remove a image from your ipfs it can be unpinned by running the function `ipfs.unpin_ipfs(CID)` where CID is the ipfs has of the corresponding image/file.

## Notes
* Each time the script is run the previous generations are overwriten but if uploaded those previous iterations will persist.


## TODO
* Add functioning Probability system. Steps have been taken in preperation for this but not yet implemented 
