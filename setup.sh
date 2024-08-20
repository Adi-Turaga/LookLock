#!/bin/bash

if [ -d encodings ] && [ -d .cache ]; then
	echo "Folders already exist"
fi

if [ ! -d encodings ]; then
	mkdir encodings
	touch faced.dat
	echo "Encodings file created"
fi

if [ ! -d .cache ]; then
	mkdir -p .cache/faces
	echo "Cache folder created"
fi
