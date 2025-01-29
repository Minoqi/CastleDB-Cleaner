# CastleDB Cleaner
**CastleDB Cleaner** is a single file python script that converts *CastleDB* default `.cdb` files into a `JSON` file. *CastleDBs* `.cdb` file is *technically* a `json` file, however, the way it is stored leaves a lot to be desired, as it stores the values in an array form rather than a dictionary form. This script solves that by using one of the columns of the sheet to act as the custom ID. Each line of the sheet will be stored into a dictionary using that ID column as the key making it much easier and nicer to use. Each sheet is also stored as it's own file.

# Technical Details
This script uses pythons built-in `os` and `json` libraries.

# License
Licensed under the MIT license, see `LICENSE` for more information.