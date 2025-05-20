from colorama import init, Fore, Style
from bs4 import BeautifulSoup as b
from pyfiglet import Figlet
import os, requests, json
from tqdm import tqdm

init(autoreset=True)

GREEN=f"{Fore.GREEN}{Style.BRIGHT}"
WHITE=f"{Fore.WHITE}{Style.BRIGHT}"

rp='repository'
gitX="https://github.com"
number=1

def clear():
 if os.name == "nt":
  os.system("cls")
 else:
  os.system("clear")

def banner():
 print(GREEN + Figlet(font='small').renderText("SaveRepo"))

def createFolder(name):
 if not os.path.exists(name):
  os.makedirs(name)

def downloadZip(user, file, url):
 folder=os.path.join('.', rp, user)
 createFolder(folder)
 Zip=os.path.join(folder, f'{file}.zip')
 with requests.get(url, stream=True) as r:
  r.raise_for_status()
  with open(Zip, 'wb') as f, tqdm(
   total=int(r.headers.get('content-length', 0)),
   unit='B', unit_scale=True, unit_divisor=1024,
   miniters=1, desc=file.split('/')[-1]
  ) as pbar:
   for chunk in r.iter_content(chunk_size=131072):
    f.write(chunk)
    pbar.update(len(chunk))

def download(link, nameRepo, user):
 response=requests.get(link).content
 soup=b(response, 'html.parser')
 findScript=soup.find_all('script', type='application/json', attrs={"data-target": "react-partial.embeddedData"})[-1]
 json_data = json.loads(findScript.string)
 try:
  zip_url = gitX + json_data['props']['initialPayload']['overview']['codeButton']['local']['platformInfo']['zipballUrl']
  folder=os.path.join('.', rp, user)
  createFolder(folder)
  Zip=os.path.join(folder, f'{nameRepo}.zip')
  if not os.path.exists(Zip):
   downloadZip(user, nameRepo, zip_url)
  else:
   print(f"{GREEN}[+]{WHITE} Ya existe {Zip}")
 except KeyError:
  pass

def showRepository(data):
 global number
 searchElement=data.find_all('a', itemprop="name codeRepository")
 for element in searchElement:
  link=gitX + element['href']
  name=link.split('/')[-1:][0] ; user=link.split('/')[-2]
  print(f'\n{GREEN}[{number}]{WHITE} {link}')
  download(link, name, user)
  number+=1

def find_element(link):
 req=requests.get(link)
 soup1=b(req.content, 'html.parser')
 showRepository(soup1)
 try:
  element_found=gitX + soup1.find_all('a', class_="next_page")[0]['href']
  find_element(element_found)
 except IndexError:
  pass

def showRepo(username):
 linkRepo=gitX + '/' +username + '?tab=repositories'
 find_element(linkRepo)

if __name__ == '__main__':
 try:
  clear()
  banner()
  username=input(f"{GREEN}[+] {WHITE}Nombre de usuario en GITHUB: " + GREEN)
  createFolder(rp)
  showRepo(username)
 except KeyboardInterrupt:
  print('\nScript Interrumpido...')
