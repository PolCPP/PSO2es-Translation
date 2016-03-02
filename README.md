# Phantasy Star Online 2 es English translation project

## Usage

1. Get the Fileco.dat from PSO2es /Android/data/com.sega.phantasystar2es/cache/sd
2. Load the Patcher tool. From https://dl.dropboxusercontent.com/u/3115520/ESBreaker.zip or https://dl.dropboxusercontent.com/u/3115520/LinuxEsBreaker.zip for a linux version.
3. Put Fileco where the tool says, json files in a json subfolder.
4. Hit the loadit button
5. Hit the load in and generate json button (this updates the pso2es database on memory), and updates the json files with new entries. Wait a few minutes. (Json lib is too slow, but since its not a process thats done every 5 min i don't care).
6. Hit save changes to save the data into a patched_fileco.dat
7. Put it back into Pso2es as fileco.dat.

## Esbreaker notes

It's possible that sega updates the game and esbreaker stops working (it will spit out some weird mambo jumbo when loading the contents database).

Just grab the current pso2es ContentsSerializer.dll, protobuf-net.dll, ProtoBuffSerializer.dll, and assembly-firstpass.dll  renamed to fp.dll and replace the files in ESBreaker_Data/Managed and it will just work.

## Credits


* SEGAC - For the libs that power the trans tool (lol)
* PolCPP - Aka Rupikachu for the tool
* AIDA - Initial translations
* Logokas - A lot of UI translation work
* Synthsy - Translation work
* Bumped.org - Item Names and Wonderful other translations
* ARKS-Visiphone - Weapon names and other neat things

## License

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004
 
 Copyright (C) 2004 Sam Hocevar
  14 rue de Plaisance, 75014 Paris, France
 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.
 
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
 
  0. You just DO WHAT THE FUCK YOU WANT TO.
