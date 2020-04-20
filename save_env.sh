if [ -z "$1" ]; then
	echo "Give env dir"
else
	source $1/bin/activate
	pip freeze > requirements.txt
	echo "Done"
fi

