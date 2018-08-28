# minecraft-symbol-analyzer
An attempt to (semi)automate the process of reverse engineer Minecraft:Bedrock Edition Headers

# Usage
put the symbol dump of nm tool into /data folder (an example of 1.5.3 placed within)
and run run.py in the same dir as run.py

and you will get your output in /data/decls

# Features & TODO
Basic reassembling ability
    (generate simple class defintions from symbols)

TODO: virtual function support

TODO: pure virtual function inference

TODO: template instantiation compression
