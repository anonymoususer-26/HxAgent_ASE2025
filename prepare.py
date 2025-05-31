import tarfile 
  
dataset = tarfile.open('./vendor/miniwob.tar.gz') 
dataset.extractall('./dataset')
dataset.close() 