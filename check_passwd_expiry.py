import subprocess

from datetime import datetime

from argparse import ArgumentParser

 

 

BUFFER_DURATION = 10 # in days

 

def get_password_expiry_from_chage(account):

  try:

    chage = subprocess.Popen(('chage', '-l', account), stdout=subprocess.PIPE)

    grep = subprocess.Popen(('grep', 'Password expires'), stdin=chage.stdout, stdout=subprocess.PIPE)

    cut = subprocess.Popen('cut -d : -f2'.split(), stdin=grep.stdout, stdout=subprocess.PIPE)

    output = cut.communicate()[0].strip()

    return output if output != 'never' else None

  except subprocess.CalledProcessError as e:

    return None

 

def is_going_to_expire(chage_date):

  expiry_date = datetime.strptime(chage_date, '%b %d, %Y')

  today = datetime.now()

  return abs((expiry_date - today).days) <= BUFFER_DURATION

 

def main():

  # Get a list of accounts from /etc/passwd

  parser = ArgumentParser(description="Password expiry notification.")

  parser.add_argument("-u", "--username", type=str, default="svcDBTK", required=False, help="mention username. default: svcDBTK")

  args = parser.parse_args()

  account = args.username

 

  chage_date = get_password_expiry_from_chage(account)

 

  if chage_date != None and is_going_to_expire(chage_date):

    print account + ' is going to expire on ' + chage_date

 

main()
