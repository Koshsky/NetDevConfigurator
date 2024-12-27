#!/bin/bash

#set -x

lang="bash"

parse_config () {
	COUNT=$(wc -l < $1)
	for (( i=1;i<=$COUNT;i++ ))
	do 
		LINE=$(head -n $i $1| tail -n  1)
		INF_LINE=$(echo $LINE | cut -d '-' -f 1) 
		PAR=$(echo $INF_LINE | cut -d ':' -f 1)
		VOL=$(echo $INF_LINE | cut -d ':' -f 2)
		PARAMS[$PAR]=$VOL
	done

}

replace () {
	sed -ri "s/<$1>/$2/g" $3	
}

ROOT_DIR=$PWD
DIR=$(dirname ${BASH_SOURCE})
declare -A PARAMS
parse_config "$ROOT_DIR/env.param" 

TYPE_SW=${PARAMS["TYPE_SW"]}
CERT=${PARAMS["CERT"]}

case $TYPE_SW in
	
	1)
	  cat $DIR/templates/data.txt| col -b > $DIR/config.cfg
	;;
	
	2)
	  cat $DIR/templates/video.txt| col -b > $DIR/config.cfg
	;;
	
	3)
	  cat $DIR/templates/mgmt.txt| col -b > $DIR/config.cfg
	;;
	
	4)
	  OR_NUM=${PARAMS["OR_NUM"]}
	  cat $DIR/templates/tsh.txt| col -b > $DIR/config.cfg
	  replace "num_or" $OR_NUM "$DIR/config.cfg"
	;;
	5)
	  OR_NUM=${PARAMS["OR_NUM"]}
	  cat $DIR/templates/or.txt| col -b > $DIR/config.cfg
	  replace "num_or" $OR_NUM "$DIR/config.cfg"
	;;
esac

replace "sert_name" $CERT "$DIR/config.cfg"
