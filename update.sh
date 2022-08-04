#!/usr/bin/env bash

DIR="$(dirname "$0")"

COND_DIR="$DIR/condition"
RULES_FILE="msgFilterRules.dat"

function resetRulesFile() {
    rulesFile="$home/$RULES_FILE"
    [ -f "$rulesFile" ] && echo -e 'version="9"\nlogging="'${1:-'no'}'"' > "$rulesFile"
}

function update() {
    _cond="$home/$name.csv"
    
    echo "======== $name ========"
    out=$(./msgFilterRules.py -n "$name" -c "$_cond" -a "${@}" -r "$rulesFile")
    echo -e "\n$out\n"
    
    echo -e "EXTRACTED FROM: $_cond\n"
    echo -en "> [$name] Write [y/n]? " && read ans
    [ "$ans" == 'y' ] && echo "$out" > "$rulesFile"
    
    echo -e "\n++++ $rulesFile ++++\n"
    cat "$rulesFile"
    echo -e "\n---- $rulesFile ----\n"
}

function update_com_gmail_reinielfc() {
    home="$COND_DIR/com.gmail.reinielfc"
    dest="imap://reinielfc%40gmail.com@imap.gmail.com"
    
    resetRulesFile
    
    name="spam"         ;   update "AddTag"="junk" "Move to folder"="$dest/%5BGmail%5D/Spam"
    
    name="work.flag"    ;   update "Mark flagged" "Move to folder"="$dest/work"
    name="work"         ;   update "Move to folder"="$dest/$name"
    
    name="order"        ;   update "Move to folder"="$dest/$name"
    
    name="service.flag" ;   update "Mark flagged" "Move to folder"="$dest/service"
    name="service"      ;   update "Move to folder"="$dest/$name"
    
    name="finances"     ;   update "Move to folder"="$dest/$name"
    
    name="code.flag"    ;   update "Mark flagged" "Move to folder"="$dest/code"
    name="code"         ;   update "Move to folder"="$dest/$name"
}

function update_com_gmail_reyfedez1208() {
    home="$COND_DIR/com.gmail.reyfedez1208"
    dest="imap://reyfedez1208%40gmail.com@imap.gmail.com"
    
    resetRulesFile
}

function update_com_live_reyfdz96() {
    home="$COND_DIR/com.live.reyfdz96"
    dest="imap://reyfdz96%40live.com@outlook.office365.com"
    
    resetRulesFile
    
    name="junk"                         ;   update "AddTag"="junk" "Move to folder"="$dest/Junk"
    
    name="to.com.outlook.mrslater99"    ;   update "Move to folder"="$dest/$name"
    
    name="update.flag"                  ;   update "Mark flagged" "Move to folder"="$dest/update"
    name="update"                       ;   update "Move to folder"="$dest/$name"
    
    name="finances.flag"                ;   update "Mark flagged" "Move to folder"="$dest/finances"
    name="finances"                     ;   update "Move to folder"="$dest/$name"
}

function update_com_yahoo_reyfedez1208() {
    home="$COND_DIR/com.yahoo.reyfedez1208"
    dest="imap://reyfedez1208%40yahoo.com@imap.mail.yahoo.com"
    
    resetRulesFile
    
    name="bulk" ;   update "AddTag"="junk" "Move to folder"="$dest/Bulk"
}

function update_all() {
    update_com_yahoo_reyfedez1208
    update_com_gmail_reyfedez1208
    update_com_live_reyfdz96
    update_com_gmail_reinielfc
}

case $1  in
    "reyfedez1208@yahoo.com")   update_com_yahoo_reyfedez1208   ;;
    "reyfedez1208@gmail.com")   update_com_gmail_reyfedez1208   ;;
    "reyfdz96@live.com")        update_com_live_reyfdz96        ;;
    "reinielfc@gmail.com")      update_com_gmail_reinielfc      ;;
    *)                          update_all                      ;;
esac