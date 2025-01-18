sshpass -p 'milkv' scp get_query.py root@192.168.42.1:/root/alpine/root/

sshpass -p 'milkv' ssh root@192.168.42.1 'chroot /root/alpine /bin/sh -c "cd /root && source venv/bin/activate && python3 get_query.py --duration 5"'

sshpass -p 'milkv' scp -O root@192.168.42.1:/root/alpine/root/recorded_audio.wav .

python3 reduce_noise.py

