echo "Recording your Speech (Ctrl+C to Transcribe)"
arecord -D plughw:1,0 -f cd -t wav -d 5 -q -r 16000 | flac - -s -f --best --sample-rate 16000 --endian little --sign signed --channels 1 --bps 16 -o pfinal.flac
 
echo "Converting Speech to Text..."
wget -q -U "Mozilla5.0" --post-file pfinal.flac --header "Content-Type: audiox-flac; rate=16000" -O - "http://www.google.com/speech-api/v2/recognize?lang=es&client=chromium" | cut -d\" -f12 > stt.txt
 
echo "You Said"
value=`cat stt.txt`
echo "$value"
