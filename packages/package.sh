mkdir sfz
cp -f ../*.py sfz/
cp -rf ../system sfz/
cp -rf ../assets sfz/
pyxel package sfz application.py
rm -r sfz
