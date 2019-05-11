#!/bin/bash

for size in 32x32 57x57 72x72 76x76 114x114 120x120 144x144 152x152 180x180 192x192
do
	convert icon.svg -resize "$size" "icon$size.png"
done
