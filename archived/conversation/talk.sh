# Copy files to remote device
sshpass -p 'milkv' scp talk.py root@192.168.42.1:/root/alpine/root/
sshpass -p 'milkv' scp response.wav root@192.168.42.1:/root/alpine/root/

# Run commands remotely in a single ssh command
sshpass -p 'milkv' ssh root@192.168.42.1 'chroot /root/alpine /bin/sh -c "cd /root && source venv/bin/activate && python3 talk.py"'

