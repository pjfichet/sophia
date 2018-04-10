#! /bin/sh

for ID in $(seq 1485); do
	BID=$(sophia print -id $ID | grep %bid | cut -d " " -f 2)
	HID=$(sophia print -id $ID | grep %hid | cut -d " " -f 2)
	TP=$(sophia print -id $ID | grep %tp | cut -d " " -f 2 | cut -d "-" -f 1)
	VHID=$(sophia head -bid $BID -p $TP | grep %id | cut -d " " -f 2)
	VHP=$(sophia head -bid $BID -p $TP | grep %hp | cut -d " " -f 2)
	if [ "$HID" != "$VHID" ]; then
		echo -n "ID $ID: hid=$HID but should be $VHID"
		if [ "$TP" == "$VHP" ]; then
			echo -n " (text page = head page = $TP)"
		fi
		TITLE=$(sophia print -id $ID | grep %T | cut -d " " -f 2-)
		echo " $TITLE"
	fi
done


