import os
os.system('pip install -r requirements.txt')
current_path = os.getcwd()
print(current_path)
os.system('cd ~')
prof_path = os.getenv("HOME")
print(prof_path)
os.system('mkdir ~/.8')
os.system('cp '+current_path+'/8.py ~/.8')
with open (prof_path+'/.profile','a') as f:
	f.write('PATH="$PATH:~/.8"')