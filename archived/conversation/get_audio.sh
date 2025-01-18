# copy test script
sshpass -p 'milkv' scp -O get_audio.py root@192.168.42.1:/root/alpine/root/

# run commands remotely in a single ssh command
sshpass -p 'milkv' ssh root@192.168.42.1 'chroot /root/alpine /bin/sh -c "cd /root && source venv/bin/activate && python3 get_audio.py --duration 5 && exit && scp -O root@192.168.42.1:/root/alpine/root/recorded_audio.wav ."'

# copy .wav audio back
